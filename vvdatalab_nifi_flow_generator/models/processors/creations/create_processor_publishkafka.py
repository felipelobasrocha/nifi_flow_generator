from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorPublishKafka(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('PublishKafka_1_0')
        self.config.properties={
                                "bootstrap.servers": processor_config.get("properties").get("publishkafka_1_0.bootstrap_servers", ""),
                                "security.protocol": processor_config.get("properties").get("publishkafka_1_0.security_protocol", ""),
                                "topic": processor_config.get("properties").get("publishkafka_1_0.topic", ""),
                                "acks": processor_config.get("properties").get("publishkafka_1_0.delivery_guarantee", ""),
                                "use-transactions": processor_config.get("properties").get("publishkafka_1_0.use_transactions", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)