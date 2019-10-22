from flask import Flask, render_template, redirect, url_for, request
from nipyapi import security
from vvdatalab_nifi_flow_generator import models
from vvdatalab_nifi_flow_generator import adapter
from vvdatalab_nifi_flow_generator import di
from vvdatalab_nifi_flow_generator import app

import json

CreateProcessGroup = models.CreateProcessGroup
CreateConnection = models.CreateConnection
CreateProcessor = models.CreateProcessor
NifiComponent = models.NifiComponent
CreateLocation = models.CreateLocation
LocationType = models.LocationType
LinkComponent = models.LinkComponent

@app.route('/default', methods=['GET', 'POST'])
def default():
    try:
        return_message = 'The Data Flow has been created'
        if request.method == 'POST':
            access = security.get_service_access_status('nifi', True)
            if access.access_status.status == 'UNKNOWN':
                error = None
                return render_template('login.html', error=error)

            raw_data = json.loads(json.loads(request.data)["process_group"])
            parent_group = adapter.to_process_group(json_process_group=raw_data)

            processor_config = raw_data["config"]
            flow_components = raw_data["flow_components"]
            group_name = raw_data["group_name"]
            group_location = raw_data["group_location"]

            create_flow(flow_components, parent_group, group_name, group_location, processor_config)

    except Exception as e:
        return_message = str(e)

    return return_message

def create_flow(flow_components, parent_group, group_name, group_location, processor_config):
    nifi_components = None
    component_location = CreateLocation(x=0.0, y=0.0, type=LocationType.ZIGZAG).create

    new_process_group = CreateProcessGroup(parent_group, group_name, (group_location["x"],group_location["y"])).create()

    for flow_component in flow_components:
        component_type = flow_component[1]
        component_name = flow_component[0]

        processor_config["properties"], component_type = map_mutliple_same_processors(processor_config, component_type)

        data = adapter.to_processor_data(new_process_group, component_name, component_location(), processor_config)

        nifi_component = create_component(component_type, data)
        nifi_components = create_connection(new_process_group, nifi_components, nifi_component)

def create_component(component_type, data):
    nifi_component = di.Factory.make_nifi_component(component_type, data)
    nifi_component.create()
    return nifi_component

def create_connection(process_group, nifi_components, nifi_component):
    if nifi_components == None:
        return LinkComponent(nifi_component)
    else:
        nifi_components.next = LinkComponent(nifi_component)

        data = adapter.to_connection_data(process_group, nifi_components.val, nifi_components.next.val, ["success"])
        di.Factory.make_nifi_component("Connection", data).create()

        return nifi_components.next

def map_mutliple_same_processors(processor_config, component_type):
    if "@" in component_type:
        return adapter.to_propertie(component_type.lower(), processor_config["properties"]), component_type.split("@")[0]
    else:
        return processor_config["properties"], component_type