from flask import render_template, request
from nipyapi import security
from vvdatalab_nifi_flow_generator import models
from vvdatalab_nifi_flow_generator import adapter
from vvdatalab_nifi_flow_generator import app

import json

CreateConnection = models.CreateConnection
ConnectionToInputPort = models.ConnectionToInputPort
ConnectionFromOutputPort = models.ConnectionFromOutputPort
CreateProcessorGetSFTP = models.CreateProcessorGetSFTP
CreateProcessGroup = models.CreateProcessGroup
CreateIOGroup = models.CreateIOGroup
CreateProcessorAvroSchema = models.CreateProcessorAvroSchema
CreateProcessorReplaceText = models.CreateProcessorReplaceText
CreateProcessorPutHiveQl = models.CreateProcessorPutHiveQl
CreateProcessorQueryRecord = models.CreateProcessorQueryRecord
CreateProcessorSplitJson = models.CreateProcessorSplitJson
CreateProcessorEvaluateJsonPath = models.CreateProcessorEvaluateJsonPath
CreateProcessorQueryInsertValues = models.CreateProcessorQueryInsertValues
CreateProcessorMergeContent = models.CreateProcessorMergeContent
CreateProcessorConstructQuery = models.CreateProcessorConstructQuery

@app.route('/mroi', methods=['GET', 'POST'])
def mroi():
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
            group_name = raw_data["group_name"]

            new_process_group = CreateProcessGroup(
                parent_group, group_name, (700.00, 700.0)).create()

            create_mroi_data_flow(new_process_group, processor_config)
    except Exception as e:
        return_message = str(e)

    return return_message

def create_mroi_data_flow(process_group, processor_config):
    processors = []

    processors.append(CreateProcessorGetSFTP(process_group, "BuscarArquivoSftp", (500.0, 400.0), processor_config))
    processors.append(CreateProcessorAvroSchema(process_group, "InformarSchema", (1500.0, 400.0), processor_config))
    processors.append(CreateProcessorQueryRecord(process_group, "CriarQuery", (1500.0, 600.0), processor_config))
    processors.append(CreateProcessorSplitJson(process_group, "SplitJson", (1500.0, 800.0), processor_config))
    processors.append(CreateProcessorEvaluateJsonPath(process_group, "MapeiaCamposJSON", (1000.0, 800.0), processor_config))
    processors.append(CreateProcessorQueryInsertValues(process_group, "MontaDados", (500.0, 800.0), processor_config))
    group_lines = CreateProcessorMergeContent(process_group, "GroupLines", (500.0, 600.0), processor_config)
    processors.append(group_lines)
    insert_hive = CreateProcessorPutHiveQl(process_group, "InsertHive", (300.0,600.0), processor_config)
    processors.append(insert_hive)

    for processor in processors:
        processor.create()

    create_mroi_sub_group(process_group, group_lines, insert_hive, processor_config)
    create_connections(process_group, processors)

def create_mroi_sub_group(new_process_group, processor_sending, processor_receiving, processor_config):
    def connect_to_sub_group(process_group, sub_process_group, processor_to_connect, input_port):
        ConnectionToInputPort(process_group, sub_process_group,
            "connection_in", processor_to_connect, input_port, ["success"]).create()     
            
    def connect_from_sub_group(process_group, sub_process_group, processor_to_connect, output_port):
        ConnectionFromOutputPort(process_group, sub_process_group,
            "connection_out", output_port, processor_to_connect, []).create(sub_process_group)

        construct_query = CreateProcessorConstructQuery(
            process_group, "ConstructQuery", (1000.0, 800.0), processor_config).create()

        CreateConnection(process_group, "input_port_to_processor", construct_query[0], construct_query[1], ["success"]).create()
        CreateConnection(process_group, "input_port_to_processor", construct_query[1], output_port, ["success"]).create("OUTPUT_PORT")

    CreateIOGroup().create(new_process_group, processor_sending, processor_receiving,
        connect_to_sub_group, connect_from_sub_group)

def create_connections(process_group, processors):
    for i in range(0,len(processors)):
        if i==len(processors)-1:
            CreateConnection(
                process_group, "connection"+str(i+1), processors[len(processors)-1], processors[len(processors)-1], ["success"]
            ).create()
            break
        CreateConnection(
            process_group, "connection"+str(i+1), processors[i], processors[i+1], ["success"]
        ).create()