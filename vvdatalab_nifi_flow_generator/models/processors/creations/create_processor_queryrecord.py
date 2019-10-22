from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorQueryRecord(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('QueryRecord')
        self.config.properties={
                                "record-reader": processor_config.get("properties").get("queryrecord.record_reader", ""),
                                "record-writer": processor_config.get("properties").get("queryrecord.record_writer", ""),
                                "include-zero-record-flowfiles": processor_config.get("properties").get("queryrecord.include_zero_record_flowfiles", ""),
                                "cache-schema": processor_config.get("properties").get("queryrecord.cache_schema", ""),
                                "queryOk": processor_config.get("properties").get("queryrecord.queryOk", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)