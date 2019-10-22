from nipyapi import canvas, nifi
from .create_processor import CreateProcessor

class CreateProcessorMergeContent(CreateProcessor):

    type = None

    def __init__(self, process_group, processor_name, processor_location, processor_config):
        CreateProcessor.__init__(self, process_group, processor_name, processor_location, processor_config)
        self.type = canvas.get_processor_type('MergeContent')
        self.config.properties={
                                "Minimum Number of Entries": processor_config.get("properties").get("mergecontent.min_number_entries", ""),
                                "Maximum Number of Entries": processor_config.get("properties").get("mergecontent.max_number_entries", ""),
                                "Delimiter Strategy": processor_config.get("properties").get("mergecontent.delimiter_strategy", ""),
                                "Tar Modified Time": processor_config.get("properties").get("mergecontent.tar_modified_time", "")
                                }

    def create(self):        
        return CreateProcessor.create(self,self.type)