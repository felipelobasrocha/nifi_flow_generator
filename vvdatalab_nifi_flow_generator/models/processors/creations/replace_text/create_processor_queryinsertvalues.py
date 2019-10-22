from nipyapi import canvas, nifi
from .create_processor_replacetext import CreateProcessorReplaceText
import json

class CreateProcessorQueryInsertValues(CreateProcessorReplaceText):

    type = None

    def __init__(self, process_group, processor_name, location, processor_config):
        CreateProcessorReplaceText.__init__(self, process_group, processor_name, location, processor_config)
        self.config.properties={
                                "Regular Expression": processor_config.get("properties").get("insertvalues.search_value", "")
                                }

        replacement_value = '('
        for field in str(processor_config.get("properties").get("insertvalues.schema", "")).split(','):
            replacement_value += '"${' + str(field) + '}",'
        
        self.config.properties.update({"Replacement Value": replacement_value[:-1] + ')' + \
            processor_config.get("properties").get("insertvalues.replacement_value", "")})

    def create(self):        
        return CreateProcessorReplaceText.create(self)