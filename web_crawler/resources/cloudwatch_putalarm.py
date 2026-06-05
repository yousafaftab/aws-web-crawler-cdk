import boto3

class cloudwatchPutAlarm:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    #function that creates alarms to be monitored on cloudwatch
    def putAlarm(self,AlarmName,AlarmActions,AlarmDescription,MetricName,namespace,dimensions,comparisonOperator,threshold):
        
        response = self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmDescription = AlarmDescription,
            AlarmActions = AlarmActions,
            MetricName = MetricName,
            Namespace = namespace,
            Dimensions = dimensions,
            ComparisonOperator = comparisonOperator,
            Threshold = threshold,
            EvaluationPeriods =1, 
            Period = 180,
            Statistic='Average'
                                    
        )

        return response
