from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorRouteOnAttribute(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('RouteOnAttribute')
        self.config.properties={
                                "Routing Strategy": processor_config.get("properties").get("routeonattribute.routing_strategy", ""),
                                "Insert": processor_config.get("properties").get("routeonattribute.routeon_insert", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)