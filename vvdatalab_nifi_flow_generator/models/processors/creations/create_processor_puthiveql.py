from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorPutHiveQl(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('PutHiveQL')
        self.config.properties={
                                "Hive Database Connection Pooling Service": processor_config.get("properties").get("puthiveql.hive_Database_connection_pooling_service", ""),
                                "hive-batch-size": processor_config.get("properties").get("puthiveql.hive_batch_size", ""),
                                "hive-charset": processor_config.get("properties").get("puthiveql.hive_chartset", ""),
                                "statement-delimiter": processor_config.get("properties").get("puthiveql.statement_delimiter", ""),
                                "rollback-on-failure": processor_config.get("properties").get("puthiveql.rollback_on_failure", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)