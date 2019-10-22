from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorFetchHDFS(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('FetchHDFS')
        self.config.properties={
                                "Hadoop Configuration Resources": processor_config.get("properties").get("fetchhdfs.hadoop_configuration_resources", ""),
                                "Kerberos Principal": processor_config.get("properties").get("fetchhdfs.kerberos_principal", ""),
                                "Kerberos Keytab": processor_config.get("properties").get("fetchhdfs.kerberos_keytab", ""),
                                "Kerberos Relogin Period": processor_config.get("properties").get("fetchhdfs.kerberos_relogin_period", ""),
                                "Additional Classpath Resources": processor_config.get("properties").get("fetchhdfs.additional_classpath_resources", ""),
                                "HDFS Filename": processor_config.get("properties").get("fetchhdfs.hdfs_file_name", ""),
                                "Compression codec": processor_config.get("properties").get("fetchhdfs.compression_codec", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)