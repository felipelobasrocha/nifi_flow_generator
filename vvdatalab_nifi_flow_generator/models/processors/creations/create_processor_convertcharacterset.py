from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorConvertCharacterSet(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('ConvertCharacterSet')
        self.config.properties={
                                "Input Character Set": processor_config.get("properties").get("convertcharacterset.input_character_set", ""),
                                "Output Character Set": processor_config.get("properties").get("convertcharacterset.output_character_set", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)