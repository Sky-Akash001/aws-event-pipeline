from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_s3_notifications as s3n,
    aws_lambda_event_sources as event_sources
)
from constructs import Construct

class AwsEventPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "MyBucket2")

        queue = sqs.Queue(self, "MyQueue2")

        producer = _lambda.Function(
            self, "ProducerLambda",
            runtime = _lambda.Runtime.PYTHON_3_11,
            handler = "producer.handler",
            code = _lambda.Code.from_asset("lambda"),
            environment = {
                "QUEUE_URL": queue.queue_url
            }
        )

        queue.grant_send_messages(producer)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(producer)
        )

        consumer = _lambda.Function(
            self, "ConsumerLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="consumer.handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        consumer.add_event_source(
            event_sources.SqsEventSource(queue)
        )
