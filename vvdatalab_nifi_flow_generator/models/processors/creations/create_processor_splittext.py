from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorSplitText(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('SplitText')
        self.config.properties={
                                "Line Split Count": processor_config.get("properties").get("splittext.line_split_count", ""),
                                "Header Line Count": processor_config.get("properties").get("splittext.header_line_count", ""),
                                "Remove Trailing Newlines": processor_config.get("properties").get("splittext.remove_trailing_newlines", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)


