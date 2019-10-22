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
CreateProcessorRouteText = models.CreateProcessorRouteText
CreateProcessGroup = models.CreateProcessGroup
CreateIOGroup = models.CreateIOGroup
CreateProcessorUpdateAttribute = models.CreateProcessorUpdateAttribute
CreateProcessorConvertRecord = models.CreateProcessorConvertRecord
CreateProcessorConvertAvroToOrc = models.CreateProcessorConvertAvroToOrc
CreateProcessorPutHDFS = models.CreateProcessorPutHDFS
CreateProcessorReplaceText = models.CreateProcessorReplaceText
CreateProcessorPutHiveQl = models.CreateProcessorPutHiveQl
CreateProcessorAvroSchema = models.CreateProcessorAvroSchema


@app.route('/template1', methods=['GET', 'POST'])
def template1():
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

            new_process_group = CreateProcessGroup(parent_group, group_name, (200.0,300.0))
            new_process_group.create()
            
            put_hdfs = CreateProcessorPutHDFS(new_process_group, "InsereArquivoNOHDFS", (100.0, 900.0), processor_config)
            put_hdfs.create()

            get_ftp = CreateProcessorGetSFTP(new_process_group, "test1", (400.0, 900.0), processor_config)
            get_ftp.create()

            connection = CreateConnection(new_process_group, "connection", put_hdfs, get_ftp, ['sucesss'])
            connection.create()
    except Exception as e:
        return_message = str(e)

    return return_message            


@app.route('/csvAvroOrcHive', methods=['GET', 'POST'])
def csv_avro_orc_hive():
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
                parent_group, group_name, (700.00,400.0)).create()

            create_data_flow(new_process_group, processor_config)
    except Exception as e:
        return_message = str(e)

    return return_message

def create_data_flow(process_group, processor_config):
    buscar_arquivo_ftp = CreateProcessorGetSFTP(
        process_group, "BuscarArquivoSftp", (500.0, 400.0), processor_config)
    buscar_arquivo_ftp.create()

    retirar_header = CreateProcessorRouteText(
        process_group, "RetirarHeaderDoCsv", (1000.0, 400.0), processor_config)
    retirar_header.create()

    informar_schema = CreateProcessorAvroSchema(
        process_group, "InformarSchema", (1500.0, 400.0), processor_config)
    informar_schema.create()

    converter_registro = CreateProcessorConvertRecord(
        process_group, "ConverterRegistrosCsvParaAvro", (1500.0, 600.0), processor_config)
    converter_registro.create()

    converter_avro_orc = CreateProcessorConvertAvroToOrc(
        process_group, "ConverterFlowFileAvroParaOrc", (1500.0, 800.0), processor_config)
    converter_avro_orc.create()

    inserir_hdfs = CreateProcessorPutHDFS(
        process_group, "InserirArquivoNoHDFS", (1000.0, 800.0), processor_config)
    inserir_hdfs.create()

    criar_hive_comando = CreateProcessorReplaceText(
        process_group, "CriarHiveDdlCommand", (500.0, 800.0), processor_config)
    criar_hive_comando.create()

    executar_hive_comando = CreateProcessorPutHiveQl(
        process_group, "ExecutarDdlHive", (500.0, 600.0), processor_config)
    executar_hive_comando.create()

    create_connections(process_group, buscar_arquivo_ftp, retirar_header, informar_schema, 
        converter_registro, converter_avro_orc, inserir_hdfs, criar_hive_comando, executar_hive_comando)

def create_connections(process_group, buscar_arquivo_ftp, retirar_header, informar_schema, 
    converter_registro, converter_avro_orc, inserir_hdfs, criar_hive_comando, executar_hive_comando):
    CreateConnection(
        process_group, "connection1", buscar_arquivo_ftp, retirar_header, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection2", retirar_header, informar_schema, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection3", informar_schema, converter_registro, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection4", converter_registro, converter_avro_orc, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection5", converter_avro_orc, inserir_hdfs, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection6", inserir_hdfs, criar_hive_comando, ["success"]
    ).create()

    CreateConnection(
        process_group, "connection7", criar_hive_comando, executar_hive_comando, ["success"]
    ).create()