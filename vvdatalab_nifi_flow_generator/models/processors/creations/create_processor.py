from nipyapi import canvas, nifi
from vvdatalab_nifi_flow_generator.models.nifi_component import NifiComponent

class CreateProcessor(NifiComponent):
  
    group = None
    name = ''
    location = ()
    config = None
    id = ''

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        self.group = process_group
        self.name = processor_name
        self.location = processor_location
        self.config = nifi.ProcessorConfigDTO(
            penalty_duration=processor_config["penalty_duration"],
            yield_duration=processor_config["yield_duration"],
            bulletin_level=processor_config["bulletin_level"],
            auto_terminated_relationships=processor_config["auto_terminated_relationships"],
            scheduling_strategy=processor_config["scheduling_strategy"],
            concurrently_schedulable_task_count=processor_config["concurrently_schedulable_task_count"],
            scheduling_period=processor_config["scheduling_period"],
            execution_node=processor_config["execution_node"],
            run_duration_millis=processor_config["run_duration_millis"],
            properties=None
        )

    def create(self, processor_type):
        processor = canvas.create_processor(
            parent_pg=self.group,
            processor=processor_type,
            location=self.location,
            name=self.name,
            config=self.config
        )
        self.id = processor.id

        return processor