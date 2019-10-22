from nipyapi import canvas, nifi

class CreateOutputPort:
  
    group = None
    location = ()
    name = ''

    def __init__(self, process_group, location, output_port_name):
        self.group=process_group
        self.location=location
        self.name=output_port_name

    def create(self):
        return canvas.create_output_port(
            parent_pg=self.group,
            location=self.location,
            output_port=nifi.PortDTO(
                parent_group_id=self.group.id,
                type="INPUT_PORT",
                name=self.name,
                position={
                    "x": self.location[0],
                    "y": self.location[1]
                }
            )
        )