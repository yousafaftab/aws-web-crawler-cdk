from unicodedata import name
from aws_cdk import (
    # Duration,
    Stack,
    pipelines,
    aws_codebuild as codebuild,
    aws_codepipeline_actions as actions
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as cdk
from sprint_4.stages_stack import YousafStages
from resources import constants as constants



class yousafPipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Access the CommitId of a GitHub source in the synth
        
        #-----------Define Source on pipelines stack----------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        source = pipelines.CodePipelineSource.git_hub("yousaf2022skipq/Orion_Python", "main",
                 authentication=cdk.SecretValue.secrets_manager("github-token_yousaf"),
                 trigger = actions.GitHubTrigger('POLL'))
        
        
        ##https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        synth=pipelines.ShellStep("Synth",
              input = source,
              commands=constants.Synth_Commands,
              primary_output_directory = constants.Pipeline_output_directory )
        
        
        #--------------Build Pipeline-----------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        Yousafpipeline = pipelines.CodePipeline(self, "PipelineYousaf",
                         synth=synth,
                         docker_enabled_for_self_mutation=True)
        
        
        #-------------Unit Integration Test------------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
        unitTest = pipelines.ShellStep ("Unit_Test",
                   input = source,
                   commands = constants.Unit_test_commands
        )

        integrationTest = pipelines.ShellStep ("Integration_Test",
                    input=source,
                    commands=constants.Integration_Test_commands
        )

        


    #     Yousafpipeline.add_wave("YousafWave",
    #         post=[
    #             pipelines.CodeBuildStep("RunApproval",
    #             commands=[],
    #             build_environment=codebuild.BuildEnvironment(
    #                 build_image=codebuild.LinuxBuildImage.from_ecr_repository(
    #                     repository="315997497220.dkr.ecr.us-east-2.amazonaws.com/beta-yousafpipelinestage-yousafecrrepositoryc8b1e1fb-f7decnxofrap"

    #                 )
    #             )
    #         )
            
    #     ]
    # )


        # pyresttest = pipelines.CodeBuildStep(
        #     "pyrest_test", commands= [],
        #     build_environment= codebuild.BuildEnvironment (
        #         build_image = codebuild.LinuxBuildImage.from_asset(self,"YousafImage", directory = "./pyrest"),
        #         privileged = True
        #     ),
        #     partial_build_spec= codebuild.BuildSpec.from_object(
        #         {
        #             "version": 0.2,
        #             "phases":{
        #                 "install":{
        #                     "commands": [ 
        #                 "- nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
        #                 "- timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""]
        #                 },
        #             "pre_build":{
        #                 "commands":[
        #                     "cd Sprint_5/pyrest",
        #                     "sudo docker build -t api-test ."
        #                 ]
        #             },
        #             "build":{
        #                 "commands": [
        #                     "sudo service docker status",
        #                     "sudo service docker start",
        #                     "sudo docker run api-test"
        #                 ]
        #             }
        #             }
        #         }
        #     )
        # )
        
        
        betaStage = YousafStages(self, "beta", env=cdk.Environment(account='315997497220', region='us-east-2'))
        #GamaStage = YousafStages(self, "Gama", env=cdk.Environment(account='315997497220', region='us-east-2'))
        prodStage = YousafStages(self, "prod", env=cdk.Environment(account='315997497220', region='us-east-2'))
        
        
        #----------------Manual Approval Step---------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/Step.html
        steps = pipelines.ManualApprovalStep("beta")
        
        
        #----------------Stages-------------------#
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/StageDeployment.html
        Yousafpipeline.add_stage(betaStage, pre = [unitTest], post=[integrationTest])
        #Yousafpipeline.add_stage(GamaStage)
        Yousafpipeline.add_stage(prodStage, pre = [steps])