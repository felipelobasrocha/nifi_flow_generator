from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorGenerateFlowFile(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('GenerateFlowFile')
        self.config.properties={
                                "generate-ff-custom-text": processor_config.get("properties").get("custom_text", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)