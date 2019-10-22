from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorSplitJson(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('SplitJson')
        self.config.properties={
                                "JsonPath Expression": processor_config.get("properties").get("splitjson.jsonpath_expression", ""),
                                "Null Value Representation": processor_config.get("properties").get("splitjson.null_value_representation", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)