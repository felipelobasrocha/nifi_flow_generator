from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorAttributesToJson(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('AttributesToJSON')
        self.config.properties={
                                "Attributes List": processor_config.get("properties").get("attributestojson.attributes_list", ""),
                                "attributes-to-json-regex": processor_config.get("properties").get("attributestojson.attributes_to_json_regex", ""),
                                "Destination": processor_config.get("properties").get("attributestojson.destination", ""),
                                "Include Core Attributes": processor_config.get("properties").get("attributestojson.include_core_attributes", ""),
                                "Null Value": processor_config.get("properties").get("attributestojson.null_value", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)