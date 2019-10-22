from nipyapi import canvas, nifi
from .create_connection import CreateConnection

class ConnectionToInputPort(CreateConnection):

    destination_type = None
    destination_group = None

    def __init__(self, process_group, destination_group, connection_name, source, destination, selected_relationships):
        CreateConnection.__init__(self, process_group, connection_name, source, destination, selected_relationships)
        self.destination_type = 'INPUT_PORT'
        self.destination_group = destination_group

    def create(self):        
        return CreateConnection.create(self, self.destination_type, self.destination_group)