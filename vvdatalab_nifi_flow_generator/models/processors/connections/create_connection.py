from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator.models.nifi_component import NifiComponent

class CreateConnection(NifiComponent):
  
    group = None
    name = ''
    source = None
    destination = None
    selected_relationships = []

    def __init__(self, process_group, connection_name, source, destination, selected_relationships):
        self.group=process_group
        self.name=connection_name
        self.source=source
        self.destination=destination
        self.selected_relationships=selected_relationships

    def create(self, destination_type = None, destination_group = None):
        if destination_group == None:
            destination_group = self.group
        
        if destination_type == None:
            destination_type = 'PROCESSOR'

        canvas.create_connection(
            parent_pg=self.group,
            connection=nifi.ConnectionDTO(
                source=nifi.ConnectableDTO(
                    id=self.source.id,
                    type='PROCESSOR',
                    group_id=self.group.id
                ),
                destination=nifi.ConnectableDTO(
                    id=self.destination.id,
                    type=destination_type,
                    group_id=destination_group.id
                ),
            selected_relationships=self.selected_relationships,
            ),
            name=self.name
        )

        return self.destination