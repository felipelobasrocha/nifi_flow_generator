from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorRouteText(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, location, processor_config)
        self.type = canvas.get_processor_type('RouteText')
        self.config.properties={
                                "Routing Strategy": processor_config.get("properties").get("routetext.routing_strategy", ""),
                                "Matching Strategy": processor_config.get("properties").get("routetext.matching_strategy", ""),
                                "Character Set": processor_config.get("properties").get("routetext.character_set", ""),
                                "Ignore Leading/Trailing Whitespace": processor_config.get("properties").get("routetext.ignore_leading_trailing_whitespace", ""),
                                "Ignore Case": processor_config.get("properties").get("routetext.ignore_case", ""),
                                "Grouping Regular Expression": processor_config.get("properties").get("routetext.grouping_regular_expression", ""),
                                "header": processor_config.get("properties").get("routetext.header", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)