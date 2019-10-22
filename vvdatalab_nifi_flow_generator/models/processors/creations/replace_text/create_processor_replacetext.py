from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator.models.processors.creations.create_processor import CreateProcessor

class CreateProcessorReplaceText(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('ReplaceText')[1]
        self.config.properties={
                                "Regular Expression": processor_config.get("properties").get("replacetext.search_value", ""),
                                "Replacement Value": processor_config.get("properties").get("replacetext.replacement_value", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)