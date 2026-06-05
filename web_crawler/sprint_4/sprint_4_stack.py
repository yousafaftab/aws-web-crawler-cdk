from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_events as events_,
    Duration,
    aws_events_targets as targets_ ,
    aws_cloudwatch as cloudwatch_ ,
    aws_iam as iam,
    aws_s3 as s3_,
    aws_s3_deployment as s3_dep,
    aws_sns as sns_,
    aws_sns_subscriptions as sub_,
    aws_cloudwatch_actions as act_,
    aws_codedeploy as codedeploy,
    aws_dynamodb as db,
    aws_lambda_event_sources as es,
    aws_apigateway as apigw,
    aws_ecr as ecr,
    aws_ecr_assets as ecr_assets,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_elasticloadbalancingv2 as elbv2
    # aws_sqs as sqs,
)
from constructs import Construct
from resources import constants as constants
import cdk_ecr_deployment as ecrdeploy
import os
from aws_cdk.aws_lambda_event_sources import SnsEventSource




class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #Create lambda function.
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        lambda_role = self.create_lambda_role()
        ApiLambda = self.create_lambda("yousafWebcrawlerApi", "./resources", "WHApihandler.lambda_handler",lambda_role)
        DBlambda = self.create_lambda("YousafAftab_DBL", './resources','DBlambda.lambda_handler',lambda_role)
        WHLambda_Function = self.create_lambda("Yousaf_Aftab_WHL", './resources','WHlambda.lambda_handler',lambda_role)
        WHLambda_Function.apply_removal_policy (RemovalPolicy.DESTROY)
        DBlambda.apply_removal_policy (RemovalPolicy.DESTROY)
        ApiLambda.apply_removal_policy(RemovalPolicy.DESTROY)

        
        # ------------------ DynamoDb Table ---------------------
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
       
        #table to write alarms 
        
        yousafTable = db.Table(self,
        #id of the table
        id = "YousafDynamoDbTable",
        #Partition key attribute definition.
        partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
        #Sort key attribute definition. Default: no sort key
        sort_key= db.Attribute(name="TimeSpam", type=db.AttributeType.STRING)
        )        

        #Table to write or read URLs via HTTP requests.
        CrudTable = db.Table (self,
        #id of the table
        id = "yousafURLtable",
        #Partition key attribute definition.
        partition_key= db.Attribute(name="websiteId", type=db.AttributeType.STRING)
        )


        #Extract Table name
        tablename = yousafTable.table_name
        crudTableName = CrudTable.table_name
        #DBlambda_name = DBlambda.function_name
        

        #Table methods        
        #add table name to lambda environment
        #Grant full access to Lambda functions who want to access those tables.
        yousafTable.grant_full_access(DBlambda)
        CrudTable.grant_full_access(ApiLambda)
        CrudTable.grant_full_access(WHLambda_Function)
        #add table name to Environment so that lambda functions can access those tables.
        DBlambda.add_environment("tablename", tablename )
        ApiLambda.add_environment("crudtablename", crudTableName)
        WHLambda_Function.add_environment("crudtablename_WH", crudTableName)
        #Apply removal policy to the tables, whenever the stack is deleted, it will also destroy tables.
        yousafTable.apply_removal_policy(RemovalPolicy.DESTROY)
        CrudTable.apply_removal_policy(RemovalPolicy.DESTROY)
                
        
        #------------------REST API Gateway------------------
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html        

        # new Lambda-backed REST Api
        api = apigw.LambdaRestApi(self,
            #id of the API gateway
            "Yousaf-WH-api",
            #Lambda function that will be triggered whenever an HTTP request hits the API gateway
            handler=ApiLambda,
            #If true, route all requests to the Lambda Function. If set to false,
            #  you will need to explicitly define the API model using addResource and addMethod (or addProxy).
            #  Default: true
            proxy=False
        )


        #Api resources
        #add a health resource to api gateway i-e API_URL/health
        health = api.root.add_resource ("health")
        #add webcrwaler resource to api gateway i-e API_URL/webcrawler
        WebCrawler =api.root.add_resource("webcrawler")
        #add websites resource to api gateway i-e API_URL/websites
        Websites = api.root.add_resource ("websites")


        #Api Methods
        #Add HTTP GET method to /health resource to accept incomming HTTP GET requests from API Gateway
        health.add_method("GET")
        #Add HTTP POST method to /websites resource to accept incomming HTTP POST requests from API Gateway
        Websites.add_method("POST")
        #Add HTTP GET method to /websites resource to accept incomming HTTP GET requests from API Gateway
        Websites.add_method("GET")
        #Add HTTP PATCH method to /websites resource to accept incomming HTTP PATCH requests from API Gateway
        Websites.add_method("PATCH")
        #Add HTTP DELETE method to /websites resource to accept incomming HTTP DELETE requests from API Gateway
        Websites.add_method("DELETE")
        #Add HTTP GET method to /webcrawler resource to accept incomming HTTP GET requests from API Gateway
        WebCrawler.add_method("GET")


        #API Deployment
        deployment = apigw.Deployment(self, "YousafApiDeployment", api=api)
        

        #Invoke lambda function periodically
        #Schedule an event for 10 minute.
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Rule.html
        #
        ScheduleLambda = events_.Schedule.rate (Duration.minutes(10))
        # Target lambda function as destination.
        SetTarget = targets_.LambdaFunction (handler = WHLambda_Function)
        
        #simple notification service
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        #first define the topic
        topic = sns_.Topic(self,
        id= "SNS_URLs_Alarms")
        topic.add_subscription(sub_.EmailSubscription("yousaf.aftab.skipq@gmail.com"))
        DBlambda.add_event_source(SnsEventSource(topic))

        topicName = topic.topic_name
        WHLambda_Function.add_environment("topicName", topicName)

        #---------------------ECR--------------------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/Repository.html
        ECR = ecr.Repository(
        #Scope of the repository
        self, 
        #id of the repository
        "YousafEcrRepository",
        #Enable the scan on push when creating the repository. Default: false
        image_scan_on_push = True,
        #Determine what happens to the repository when the resource/stack is deleted. 
        # Default: RemovalPolicy.Retain
        removal_policy=RemovalPolicy.DESTROY)
        #get the repository's account resource's name
        repository_arn = ECR.repository_arn
        #get the repository's name
        repository_name = ECR.repository_name
        #gets the repository's uri.
        repository_uri = ECR.repository_uri

        

        #---------------------Docker Assets-----------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assets/DockerImageAsset.html
        #The image will be created in build time and uploaded to an ECR repository.
        #An asset that represents a Docker image.
        docker_assets = ecr_assets.DockerImageAsset (
            #Scope of the DOcker image
            self, 
            #id of the Docker image
            "docImage",
            #location where the image is stored.
            directory= "./pyrest")

        #DockerImageAsset is designed for seamless build & consumption of image assets by CDK code deployed
        #  to multiple environments through the CDK CLI or through CI/CD workflows.
        #  To that end, the ECR repository behind this construct is controlled by the AWS CDK.
        #  The mechanics of where these images are published
        #  and how are intentionally kept as an implementation detail,
        #  and the construct does not support customizations such as specifying the ECR repository name or tags.
        ecrdeploy.ECRDeployment (self, "DeployImage",
        src = ecrdeploy.DockerImageName(docker_assets.image_uri),
        dest = ecrdeploy.DockerImageName (f"{repository_uri}:latest"))


        # #-------------------EC2 VPC------------------------#
        # vpc = ec2.Vpc(self, "yousafEc2Vpc",cidr="10.0.0.0/25", max_azs= 2)


        # #--------------------ECS Cluster----------------------#
        # ecs_cluster = ecs.Cluster (self, "yousafEcsCluster",
        # cluster_name="YousafCluster",
        # container_insights=True,
        # enable_fargate_capacity_providers=True
        # )


        # #-------------------ECS task definition--------------#
        # ecs_task_role = self.create_ecs_task_role()
        # ecs_task_log = logs.LogGroup (self, "yousaf-ecs-logs",
        # retention= logs.RetentionDays.FIVE_DAYS
        # )

        # fargate_task_definition = ecs.FargateTaskDefinition(self, 
        # "yousaf-fargate-task-definition",
        # cpu=256,
        # ephemeral_storage_gib=21,
        # memory_limit_mib=512,
        # family="yousaf-ecs-task-family",
        # task_role=ecs_task_role,
        # )

        # ecs_container = fargate_task_definition.add_container(
        #     id="yousaf-Ecs-Container",
        #     image= ecs.ContainerImage.from_ecr_repository(repository=ECR),
        #     container_name= "yousaf-container",
        #     cpu=256,
        #     logging=ecs.LogDriver.aws_logs(stream_prefix="yousaf-ecs-task", log_group=ecs_task_log),
        #     essential= True,
        #     memory_limit_mib=512,
        #     memory_reservation_mib=512,
        #     privileged= True,
        #     port_mappings=[ecs.PortMapping(
        #         container_port=8081,
        #         protocol=ecs.Protocol.TCP
        #     )]
        # )

        # #------------------ECS Service------------------------#
        # ecs_service = ecs.FargateService(self, "yousaf-fargate-service",
        # service_name="yousaf-ecs-service",
        # task_definition= fargate_task_definition,
        # cluster= ecs_cluster,
        # desired_count=20,
        # max_healthy_percent= 100,
        # min_healthy_percent=20,
        # ) 


        # #-----------------Elastic load Balancer-----------------
        # lb = elbv2.ApplicationLoadBalancer (
        #     self, "yousaf-Load-Balancer",
        #     vpc=vpc,
        #     internet_facing= True
        # )
        # listener = lb.add_listener(
        #     "yousaf-listener",
        #     port=80
        # )
        # ecs_service.register_load_balancer_targets(
        #     ecs.EcsTarget(
        #         container_name= "yousaf-container",
        #         new_target_group_id="ECS",
        #         listener=ecs.ListenerConfig.application_listener(
        #             listener,
        #             protocol= elbv2.ApplicationProtocol.HTTP
        #         )
        #     )
        # )


        #-----------------Lambda Metrics----------------------
        f_name = WHLambda_Function.function_name    
        #-----------------Metric Dimensions-------------------
        Lambda_Dim = {"FunctionName": f_name}
        
        
        #-----------------Error Metric------------------------
        Lambda_Errors_Metric = cloudwatch_.Metric (metric_name ="Errors",
        namespace = "AWS/Lambda",
        dimensions_map = Lambda_Dim
        )
        
        
        #----------------Error Alarm--------------------------
        Lambda_Error_Alarm = cloudwatch_.Alarm(self,
        id = "Lambda_Error",
        metric = Lambda_Errors_Metric,
        evaluation_periods =1,
        threshold = 5,
        comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm = 1)
        
        
        #-----------------Invocation Metric-------------------
        Lambda_Invocations_Metric = cloudwatch_.Metric (metric_name ="Invocations",
        namespace = "AWS/Lambda",
        dimensions_map = Lambda_Dim
        )
        
        
        #----------------Invocation Alarm---------------------
        Lambda_Invocations_Alarm = cloudwatch_.Alarm(self,
        id = "Lambda_Invocations",
        metric = Lambda_Invocations_Metric,
        evaluation_periods =1,
        threshold = 5,
        comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm = 1)
        
        
        #-----------------CodeDeploy-----------------#
        
        #-----------------Deployment Config ----------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/CustomLambdaDeploymentConfig.html
        config = codedeploy.CustomLambdaDeploymentConfig (self,
        id = "DepConfig",
        interval = Duration.minutes (1),
        percentage =50,
        type = codedeploy.CustomLambdaDeploymentConfigType.LINEAR)
        
        
        #------------------Lambda Alias-----------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html
        alias = lambda_.Alias(self,
        "alias",
        alias_name = "alias_lambda",
        version = WHLambda_Function.current_version)
        
        
        #------------------Lambda Alarms---------------#
        alarms = [Lambda_Invocations_Alarm, Lambda_Error_Alarm]

        #------------------AutoRollbackConfig----------#
        AutoRollback = codedeploy.AutoRollbackConfig(
            deployment_in_alarm= True,
            failed_deployment= True,
            stopped_deployment= True
        )
                
        
        #-------------------Deployment Group-------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployment_group = codedeploy.LambdaDeploymentGroup(self,
        id = "YousafDeployment",
        alias = alias,
        deployment_config = config,     #codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        alarms = alarms,
        auto_rollback=AutoRollback
        )
                
        
        #----------------define rule to invoke lambda function.
        Rule = events_.Rule (self,
        id = "Yousaf_Lambda_Invoke",
        description = "My lambda function will invoke after every 10 minute ",
        enabled = True,
        schedule = ScheduleLambda,
        targets = [SetTarget]
            )
        
    
    #Function that triger lambda service    
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function (self,
            id = id,
            code = lambda_.Code.from_asset(asset),
            handler = handler,
            runtime = lambda_.Runtime.PYTHON_3_6,
            role = role,
            timeout = Duration.seconds(120)
            )


    
    def create_lambda_role (self):
        #Define role to access cloudwatch.
        Role = iam.Role(self, "lambda-role",
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com"),
             managed_policies = [
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole') ,
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaInvocation-DynamoDB")
             ]
            )
        return Role    
    
    def create_ecs_task_role(self):
        sts_policy = iam.PolicyStatement(actions=['sts:AssumeRole'], resources=['*'])
        cw_policy = iam.PolicyStatement(actions=['logs:*'], resources=['*'])
        task_role_policy_document = iam.PolicyDocument(statements= [sts_policy,cw_policy])
        return iam.Role(self, "yousaf-ecs-task-role",
        assumed_by= iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        description="ECS task role for package forecast app",
        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")],
        inline_policies=[task_role_policy_document]
        )
