#!/usr/bin/env python3
import os

import aws_cdk as cdk

#from sprint_3.sprint_3_stack import Sprint3Stack
from sprint_4.yousafPipelineStack import yousafPipeline


app = cdk.App()
app = cdk.App()
cdk.Tags.of(app).add ("Cohort","Orion")
cdk.Tags.of(app).add ("Name","Yousaf Aftab")
yousafPipeline(app, "YousafPipeline",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account='315997497220', region='us-east-2'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
