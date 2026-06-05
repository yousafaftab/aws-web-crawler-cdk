import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint_4.sprint_4_stack import Sprint4Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint_4/sprint_4_stack.py

def test_S3_queue_created():
    app = core.App()
    stack = Sprint4Stack(app, "sprint-4")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::S3::Bucket", 0 )

