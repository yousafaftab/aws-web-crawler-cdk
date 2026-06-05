from aws_cdk import (
    # Duration,
    Stage,
    # aws_sqs as sqs,
)
from constructs import Construct
from sprint_4.sprint_4_stack import Sprint4Stack

class YousafStages(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stage = Sprint4Stack ( self, "YousafPipelineStage")
