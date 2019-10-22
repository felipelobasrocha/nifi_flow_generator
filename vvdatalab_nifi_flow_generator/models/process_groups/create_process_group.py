from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator.models.nifi_component import NifiComponent

class CreateProcessGroup(NifiComponent):
  
    parent = None
    name = ''
    location = ()
    id = ''

    def __init__(self, parent_group, group_name, group_location):
        self.parent = parent_group
        self.name = group_name
        self.location = group_location

    def create(self):
        new_process_group = canvas.create_process_group(
            self.parent,
            self.name,
            self.location
        )
        new_process_group.revision.version = 0
        self.id = new_process_group.id

        return new_process_group