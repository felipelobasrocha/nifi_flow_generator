from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorConsumeKafka(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('ConsumeKafka_0_10')
        self.config.properties={
                                "bootstrap.servers": processor_config.get("properties").get("consumekafka_0_10.bootstrap_servers", ""),
                                "security.protocol": processor_config.get("properties").get("consumekafka_0_10.security_protocol", ""),
                                "topic": processor_config.get("properties").get("consumekafka_0_10.topic", ""),
                                "topic_type": processor_config.get("properties").get("consumekafka_0_10.topic_type", ""),
                                "group.id": processor_config.get("properties").get("consumekafka_0_10.group_id", ""),
                                "auto.offset.reset": processor_config.get("properties").get("consumekafka_0_10.latest", ""),
                                "key-attribute-encoding": processor_config.get("properties").get("consumekafka_0_10.key_attribute_encoding", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)