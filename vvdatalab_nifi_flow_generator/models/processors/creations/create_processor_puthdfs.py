from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorPutHDFS(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('PutHDFS')
        self.config.properties={
                                "Hadoop Configuration Resources": processor_config.get("properties").get("puthdfs.hadoop_configuration_resources", ""),
                                "Kerberos Principal": processor_config.get("properties").get("puthdfs.kerberos_principal", ""),
                                "Kerberos Keytab": processor_config.get("properties").get("puthdfs.kerberos_keytab", ""),
                                "Kerberos Relogin Period": processor_config.get("properties").get("puthdfs.kerberos_relogin_period", ""),
                                "Additional Classpath Resources": processor_config.get("properties").get("puthdfs.additional_classpath_resources", ""),
                                "Directory": processor_config.get("properties").get("puthdfs.directory", ""),
                                "Conflict Resolution Strategy": processor_config.get("properties").get("puthdfs.conflict_resolution_strategy", ""),
                                "Compression codec": processor_config.get("properties").get("puthdfs.compression_codec", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)