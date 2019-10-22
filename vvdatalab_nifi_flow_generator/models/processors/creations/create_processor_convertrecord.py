from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorConvertRecord(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, location, processor_config)
        self.type = canvas.get_processor_type('ConvertRecord')
        self.config.properties={
                                "record-reader": processor_config.get("properties").get("convertrecord.record_reader", ""),
                                "record-writer": processor_config.get("properties").get("convertrecord.record_writer", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)