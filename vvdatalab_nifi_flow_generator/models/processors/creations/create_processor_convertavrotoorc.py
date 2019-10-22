from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorConvertAvroToOrc(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, location, processor_config)
        self.type = canvas.get_processor_type('ConvertAvroToORC')
        self.config.properties={
                                "orc-config-resources": processor_config.get("properties").get("convertavrotoorc.orc_config_resources", ""),
                                "orc-stripe-size": processor_config.get("properties").get("convertavrotoorc.orc_stripe_size", ""),
                                "orc-buffer-size": processor_config.get("properties").get("convertavrotoorc.orc_buffer_size", ""),
                                "orc-compression-type": processor_config.get("properties").get("convertavrotoorc.orc_compression_type", ""),
                                "orc-hive-table-name": processor_config.get("properties").get("convertavrotoorc.orc_hive_table_name", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)