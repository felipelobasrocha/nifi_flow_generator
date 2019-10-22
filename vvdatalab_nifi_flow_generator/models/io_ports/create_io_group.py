from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator import models
from vvdatalab_nifi_flow_generator.models.io_ports.create_input_port import CreateInputPort
from vvdatalab_nifi_flow_generator.models.io_ports.create_output_port import CreateOutputPort

CreateProcessGroup = models.CreateProcessGroup
CreateLocation = models.CreateLocation
LocationType = models.LocationType

class CreateIOGroup:

    def create(self, process_group, processor_to_connect=None, processor_from_connect=None, connect_to=None,
        connect_from=None, component_location=None):

        if component_location == None:
            component_location = lambda : (2000.00, 400.0)

        io_process_group = CreateProcessGroup(
            process_group, 'IOProcessGroup', component_location()).create()

        component_location = CreateLocation(x=0.0, y=0.0, type=LocationType.ZIGZAG).create

        if processor_to_connect != None and connect_to != None:
            input_port = CreateInputPort(io_process_group, component_location(), 'input_port').create()
            connect_to(process_group, io_process_group, processor_to_connect, input_port)

        if processor_from_connect != None and connect_from != None:
            output_port = CreateOutputPort(io_process_group, component_location(), 'output_port').create()
            connect_from(io_process_group, process_group, processor_from_connect, output_port, component_location)
        
        return io_process_group