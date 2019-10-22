from flask import Flask, Blueprint, render_template, redirect, url_for, request
from nipyapi import config, canvas, security, nifi
from vvdatalab_nifi_flow_generator import models
from vvdatalab_nifi_flow_generator import adapter
from vvdatalab_nifi_flow_generator import app

import json

CreateConnection = models.CreateConnection
ConnectionToInputPort = models.ConnectionToInputPort
ConnectionFromOutputPort = models.ConnectionFromOutputPort
CreateProcessorGetSFTP = models.CreateProcessorGetSFTP
CreateProcessorRouteText = models.CreateProcessorRouteText
CreateProcessGroup = models.CreateProcessGroup
CreateIOGroup = models.CreateIOGroup
CreateProcessorUpdateAttribute = models.CreateProcessorUpdateAttribute
CreateLocation = models.CreateLocation
LocationType = models.LocationType

@app.route('/example', methods=['GET', 'POST'])
def example():
    try:
        return_message = 'OK'
        if request.method == 'POST':
            access = security.get_service_access_status('nifi', True)
            if access.access_status.status == 'UNKNOWN':
                error = None
                return render_template('login.html', error=error)

            raw_data = json.loads(request.form['process_group'])
            parent_group = adapter.to_process_group(json_process_group=raw_data)
            processor_config = raw_data["config"]

            new_process_group = CreateProcessGroup(
                parent_group, raw_data["group_name"], (700.00,400.0)).create()

            buscar_arquivo_ftp = CreateProcessorGetSFTP(
                new_process_group, "BuscarArquivoSftp", (500.0, 400.0), processor_config)
            buscar_arquivo_ftp.create()

            retirar_header = CreateProcessorRouteText(
                new_process_group, "RetirarHeaderDoCsv", (1000.0, 400.0), processor_config)
            retirar_header.create()

            CreateConnection(
                new_process_group, "buscar_arquivo_ftp_retirar_header", buscar_arquivo_ftp, retirar_header, ["success"]
            ).create()

            retirar_header_test = CreateProcessorRouteText(
                new_process_group, "RetirarHeaderDoCsvtest", (1000.0, 800.0), processor_config)
            retirar_header_test.create()

            create_sub_group_example1(new_process_group, retirar_header, retirar_header_test, processor_config)

    except Exception as e:
        return_message = str(e)

    return return_message

@app.route('/example2', methods=['GET', 'POST'])
def example2():
    try:
        return_message = 'OK'
        if request.method == 'POST':
            access = security.get_service_access_status('nifi', True)
            if access.access_status.status == 'UNKNOWN':
                error = None
                return render_template('login.html', error=error)

            raw_data = json.loads(request.form['process_group'])
            parent_group = adapter.to_process_group(json_process_group=raw_data)
            processor_config = raw_data["config"]
            group_location = raw_data["group_location"]

            component_location = CreateLocation(x=0.0, y=0.0, type=LocationType.ZIGZAG).create

            new_process_group = CreateProcessGroup(
                parent_group, raw_data["group_name"], (group_location["x"],group_location["y"])).create()

            test_update_attribute = CreateProcessorUpdateAttribute(
                new_process_group, "TestUpdateAttribute", component_location(), processor_config)
            test_update_attribute.create()

            create_sub_group_example2(new_process_group, None, test_update_attribute, processor_config, component_location)

            test_update_attribute2 = CreateProcessorUpdateAttribute(
                new_process_group, "TestUpdateAttribute2", component_location(), processor_config)
            test_update_attribute2.create()

            CreateConnection(
                new_process_group, "connection_test", test_update_attribute, test_update_attribute2, ["success"]
            ).create()            

    except Exception as e:
        return_message = str(e)

    return return_message

def create_sub_group_example1(new_process_group, processor_sending, processor_receiving, processor_config):
    def connect_to_sub_group(process_group, sub_process_group, processor_to_connect, input_port):
        ConnectionToInputPort(process_group, sub_process_group,
            "connection_in", processor_to_connect, input_port, ["success"]).create()     
            
    def connect_from_sub_group(process_group, sub_process_group, processor_to_connect, output_port):
        ConnectionFromOutputPort(process_group, sub_process_group,
            "connection_out", output_port, processor_to_connect, []).create(sub_process_group)

        processor1 = CreateProcessorGetSFTP(
            process_group, "Processor1", (500.0, 800.0), processor_config)
        processor1.create()

        processor2 = CreateProcessorGetSFTP(
            process_group, "Processor2", (1000.0, 800.0), processor_config)
        processor2.create()

        CreateConnection(
            process_group, "processor_to_processor", processor1, processor2, ["success"]
        ).create()

        CreateConnection(
            process_group, "processor_to_output_port", processor2, output_port, ["success"]
        ).create("OUTPUT_PORT")

    CreateIOGroup().create(new_process_group, processor_sending, processor_receiving,
        connect_to_sub_group, connect_from_sub_group)

def create_sub_group_example2(new_process_group, processor_sending, processor_receiving, processor_config, component_location):

    def connect_from_sub_group(process_group, sub_process_group, processor_to_connect, output_port, component_location):
        ConnectionFromOutputPort(process_group, sub_process_group,
            "connection_out", output_port, processor_to_connect, []).create(sub_process_group)

        processor1 = CreateProcessorGetSFTP(
            process_group, "Processor1", component_location(), processor_config)
        processor1.create()

        processor2 = CreateProcessorGetSFTP(
            process_group, "Processor2", component_location(), processor_config)
        processor2.create()

        CreateConnection(
            process_group, "processor_to_processor", processor1, processor2, ["success"]
        ).create()

        CreateConnection(
            process_group, "processor_to_output_port", processor2, output_port, ["success"]
        ).create("OUTPUT_PORT")

    CreateIOGroup().create(new_process_group, processor_sending, processor_receiving,
        None, connect_from_sub_group, component_location)        