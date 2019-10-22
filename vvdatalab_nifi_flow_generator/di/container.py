from vvdatalab_nifi_flow_generator import models

class Container:

    container = dict()

    def __init__(self):
        self.container = \
        {
        "GetSFTP": models.CreateProcessorGetSFTP,
        "RouteText": models.CreateProcessorRouteText,
        "UpdateAttribute": models.CreateProcessorUpdateAttribute,
        "ConvertRecord": models.CreateProcessorConvertRecord,
        "ConvertAvroToOrc": models.CreateProcessorConvertAvroToOrc,
        "PutHDFS": models.CreateProcessorPutHDFS,
        "PutHiveQl": models.CreateProcessorPutHiveQl,
        "AvroSchema": models.CreateProcessorAvroSchema,
        "QueryRecord": models.CreateProcessorQueryRecord,
        "SplitJson": models.CreateProcessorSplitJson,
        "EvaluateJsonPath": models.CreateProcessorEvaluateJsonPath,
        "InsertValues": models.CreateProcessorQueryInsertValues,
        "MergeContent": models.CreateProcessorMergeContent,
        "ReplaceText": models.CreateProcessorReplaceText,
        "ConsumeKafka_0_10": models.CreateProcessorConsumeKafka,
        "ConstructQuery": models.CreateProcessorConstructQuery
        }    

    def resolve(self, type):
        return self.container[type]