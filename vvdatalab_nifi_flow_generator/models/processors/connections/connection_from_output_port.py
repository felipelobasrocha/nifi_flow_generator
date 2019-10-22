from nipyapi import canvas, nifi
from .create_connection import CreateConnection

class ConnectionFromOutputPort(CreateConnection):

    type = None
    destination_group = None

    def __init__(self, process_group, destination_group, connection_name, source, destination, selected_relationships):
        CreateConnection.__init__(self, process_group, connection_name, source, destination, selected_relationships)
        self.type = 'OUTPUT_PORT'
        self.destination_group = destination_group

    def create(self, destination_group = None):
        if destination_group == None:
            destination_group = self.group

        canvas.create_connection(
            parent_pg=destination_group,
            connection=nifi.ConnectionDTO(
                source=nifi.ConnectableDTO(
                    id=self.source.id,
                    type=self.type,
                    group_id=self.group.id
                ),
                destination=nifi.ConnectableDTO(
                    id=self.destination.id,
                    type='PROCESSOR',
                    group_id=destination_group.id
                ),
            selected_relationships=self.selected_relationships
            ),
            name=self.name
        )

        return self.destination