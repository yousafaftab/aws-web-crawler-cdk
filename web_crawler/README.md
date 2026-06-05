
# CRUD API Gateway for Web Crawler

Create CRUD API gateway for the web crawler that will create, read, update or delete to/ from DynamoDB, write integration tests to check the functionality of the integrated resources and motitor the metrics in runtime environment and write alarms to the DynamoDB.
## Project tasks

1. Create a DynamoDB table to which the client's data to be saved or to be extraced via HTTP requests.
2. Create a lambda function that will invoke on client's HTTP requests and will interact with DynamoDB to return HTTP response to the client.
3. Create API gateway for the web crwaler, define resources and add HTPP methods to the resources.
4. Write integgration tests to check whether the lambda is invokedon HTTP requests and returns HTTP response from DynamoDB table to client.
5. Scan the DynamoDB table and extract the list of website from database and pass that list to the web crawler to calculate latency and availability of the web URLs.
6. Develop an API to monitor the metrics and create alarms on cloudWatch in a runtime environment and take actions on that alarms.
7. Create a DynamoDb to store runtime alarms.
8. Create a lambda function that will invoke when the runtime alarm is created on cloudWalth, and write those alarms to the DynamoDB table.
## DynamoDB Table for web URLs
CDK documentation link to create DynamoDB table is mentioned below.
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html

Grant full access to your lambda function that will interact with DynamoDB
Apply removal policy to your table.

Code is available in Sprint4Stack.py file



## Lambda function for HTTP requests
CDK documentation link to create lambda function is mentioned below.
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html

In your API lambda handler,
1. Access the DynamoDB table using environment variables.
2. Define HTTP methods.
3. Define paths for API.
4. Extract HTTP method and Path from your HTTP request body.
5. Compare the paths and HTTP methods with your defined CRUD functionality
6. Define CRUD functions and call them in your lambda handler.

## API Gateway
CDK documentation link to create API gameway is mentioned below.
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
After the creation of API, do the following steps
1. Define API resources
```Bash
health = api.root.add_resource ("Health")
WebCrawler =api.root.add_resource("WebCrawler")
Websites = api.root.add_resource ("Websites")
```
2. Define API methods

```
health.add_method("GET")
Websites.add_method("POST")
Websites.add_method("GET")
Websites.add_method("PATCH")
Websites.add_method("DELETE")
WebCrawler.add_method("GET")
```
## Integration tests
To create Integration test, move to your test directory from root directory and create a file that start with keyword "test", in that file, define your function that you want to perform and function name should start with keywork "test"
Test your integration tests uning pytest command on your terminal.
Add your Integration test to your pipeline stage.
## Scan DynamoDB table
1. Write a Python function that will scan DynamoDB table.
2. You can use AWS SDK boto3 client to scan the table as well.
3. Documentation link for boto3 is mentioned below.
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan

## Monitor Metrics Runtime
Boto3 documentation to create API client that will create alarms runtime is mentioned below.
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm
## Write alarms to DynamoDB
1. Create a DynamoDB table.
2. create Lambda function
3. Grant full access to the lambda function.
4. Lambda will be invoked when CloudWatch will take action on your defined topic.
5. In lambda handler file, extract your required metrics from the SNS body using python unpacking.
6. Write those metrics to dynamoDB by creating API using boto3.
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item