from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorGetSFTP(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('GetSFTP')
        self.config.properties={
                                "Hostname": processor_config.get("properties").get("getsftp.host_name", ""),
                                "Port": processor_config.get("properties").get("getsftp.port", ""),
                                "Username": processor_config.get("properties").get("getsftp.user_name", ""),
                                "Password": processor_config.get("properties").get("getsftp.password", ""),
                                "Remote Path": processor_config.get("properties").get("getsftp.remote_path", ""),
                                "File Filter Regex": processor_config.get("properties").get("getsftp.file_filter_regex", ""),
                                "Polling Interval": processor_config.get("properties").get("getsftp.polling_interval", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)