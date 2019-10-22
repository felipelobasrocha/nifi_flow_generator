from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorEvaluateJsonPath(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('EvaluateJsonPath')
        self.config.properties={
                                "Destination": processor_config.get("properties").get("evaluatejsonpath.destination", ""),
                                "Return Type": processor_config.get("properties").get("evaluatejsonpath.return_type", ""),
                                "Path Not Found Behavior": processor_config.get("properties").get("evaluatejsonpath.path_not_found_behavior", ""),
                                "Null Value Representation": processor_config.get("properties").get("evaluatejsonpath.null_value_representation", "")
                                }

        for field in str(processor_config.get("properties").get("evaluatejsonpath.schema", "")).split(','):
            self.config.properties[field] = "$."+str(field).upper()

    def create(self):        
        return CreateProcessor.create(self,self.type)