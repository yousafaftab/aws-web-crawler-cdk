import urllib3
import datetime
import boto3
import json
import logging
import os
from custom_encoder import customEncoder
import constants as constants
from cloudwatch_putmetric import cloudwatchPutMetric
from cloudwatch_putalarm import cloudwatchPutAlarm
logger = logging.getLogger()
logger.setLevel(logging.INFO)

topicname = os.getenv("topicName")

AvailabilityMetricName = 'url_availability'
LatencyMetricName = 'url_latency'
namespace = 'YousafNameSpace'
AvailabilitycomparisonOperator = 'LessThanThreshold'
latencycomparisonOperator = 'GreaterThanThreshold'
AvailabilityThreshold = 1
LatencyThreshold = 0.6
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{topicname}".format(topicname=topicname)]




#Access table through lambda function
tablename = os.getenv("crudtablename_WH")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)
web_urls = []
values = []

def lambda_handler(event, context):
    
    response = table.scan()
    result = response['Items']

    while 'lastEvaluatedKey' in response:
        response = table.scan (ExclusiveStarKey = response['LastEvaluatedKey'])
        result.extend(response['Items'])
    for x in range (len(result)):
        web_urls.append(result[x]["web_URL"])
    
    
    
    cw = cloudwatchPutMetric()
    cwa = cloudwatchPutAlarm()
    
    
    for website in web_urls:
        
        dimensions =  [
                {'Name': 'url',
                'Value': website } 
                ]
        
        AvailabilityAlarmName = "Yousaf_Availability_{web_url}".format(web_url=website)
        LatencyAlarmName = "Yousaf_Latency_{web_url}".format(web_url=website)
        AlarmDescription = "Alarm_of_{web_url}".format(web_url=website)
        
                
        avail = availability(website)
        cw.putData(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_METRIC_NAME_AVAILABILITY, dimensions, avail)
        
        cwa.putAlarm(AvailabilityAlarmName, AlarmActions, AlarmDescription, AvailabilityMetricName,
        namespace, dimensions, AvailabilitycomparisonOperator,AvailabilityThreshold)

        
        
        #get the latency of website
        lat  = latency(website)
        cw.putData(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_METRIC_NAME_LATENCY, dimensions, lat)
        
        cwa.putAlarm(LatencyAlarmName, AlarmActions, AlarmDescription,LatencyMetricName,
        namespace,dimensions,latencycomparisonOperator,LatencyThreshold)


        
        
        # update values of latency and availablity to dictionary.
        values.append(({"website": website , "availability ": avail, "latency (s)" : lat}))

        

        
        
        #return availability and latency of website.
        
    return values
    
    #cw.putLambda("AWS/Lambda","Errors",{"Metric_name ": "Lambda_Errors"})
    
def availability(website):  # returns the availability of website.
    http = urllib3.PoolManager()
    r = http.request('GET', website)
    if r.status == 200:
        return 1.0
    else:
        return 0.0




def latency(website):  #return the latency of website.
        http = urllib3.PoolManager()
        start = datetime.datetime.now()
        r = http.request('GET', website)
        end = datetime.datetime.now()
        delta = end - start
        latencySeconds = round(delta.microseconds *0.000001, 6)
        return latencySeconds