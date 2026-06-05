from unittest import result
from urllib import response
import boto3
import json
import logging
import os
from custom_encoder import customEncoder
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Access table through lambda function
tablename = "beta-YousafPipelineStage-yousafURLtableCE9EADE1-1MWLCH74B1XY8"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)
web_urls = []
response = table.scan()
result = response['Items']

while 'lastEvaluatedKey' in response:
    response = table.scan (ExclusiveStarKey = response['LastEvaluatedKey'])
    result.extend(response['Items'])
for x in range (len(result)):
    web_urls.append(result[x]["web_URL"])
print (web_urls)