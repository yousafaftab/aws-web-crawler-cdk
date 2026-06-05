import boto3
class cloudwatchPutMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        
    #function that pass metrices to be monitored on clowdwatch
    def putData(self,NameSpace, MetricName, Dimensions, Value):

        response = self.client.put_metric_data(
            Namespace=NameSpace,
            MetricData=[
                {
                    'MetricName': MetricName,
                    'Dimensions': Dimensions,
                    'Values': [Value]
                },
            ]
        )
    