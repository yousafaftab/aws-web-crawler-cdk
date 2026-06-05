from asyncio import events
import boto3
import os
import json

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    tablename = os.getenv("tablename")

    event_response = event["Records"]
    Sns_message = event_response[0]["Sns"]["Message"]
    Sns_messageid = event_response[0]["Sns"]["MessageId"]
    Sns_Timestamp = event_response[0]["Sns"]["Timestamp"]
    Sns_type = event_response[0]["Sns"]["Type"]

    response = client.put_item(
    TableName = tablename,
    Item={
        "id": {
            'S' : Sns_messageid},
        "TimeSpam": {
            'S' : Sns_Timestamp},    
            
        "SNS_TYPE": {
            'S' : Sns_type},
        
        "SNS_Message": {
            'S' : Sns_message}
        }
    )
     

   
   
    