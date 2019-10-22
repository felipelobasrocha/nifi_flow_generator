from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator.models.processors.creations.create_processor import CreateProcessor

class CreateProcessorUpdateAttribute(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, location, processor_config)
        self.type = canvas.get_processor_type('UpdateAttribute')

        self.config.properties={
                                "Delete Attributes Expression": processor_config.get("properties").get("updateattribute.delete_attribute_expression", ""),
                                "Store State": processor_config.get("properties").get("updateattribute.store_state", ""),
                                "Stateful Variables Initial Value": processor_config.get("properties").get("updateattribute.stateful_variables_initial_value", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)