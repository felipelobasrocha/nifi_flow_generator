from vvdatalab_nifi_flow_generator import models
from .container import Container

class Factory:

    @staticmethod
    def make_nifi_component(type, data):
        if type == "Connection":
            return models.CreateConnection(
                process_group=data.process_group,
                connection_name=str(data.source.name)+str(data.destination.name),
                source=data.source,
                destination=data.destination,
                selected_relationships=data.selected_relationships
            )

        return Container().resolve(type)(data.new_process_group,data.component_name,data.component_location,data.processor_config)