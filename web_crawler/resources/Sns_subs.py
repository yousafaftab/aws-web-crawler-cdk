from urllib import response
import boto3

class SNSsubscription:
    def __init__(self):
        self.client = boto3.client('sns')

    def sns_subs(self,TopicArn,Protocol,Endpoint):
        response = self.client.subscribe (
            TopicArn = TopicArn,
            Protocol = Protocol,
            Endpoint = Endpoint,
            ReturnSubscriptionArn = True
        )