import json
import boto3
import os

sqs = boto3.client('sqs')

def handler(event, context):
    print("S3 Event:", json.dumps(event))

    sqs.send_message(
        QueueUrl=os.environ['QUEUE_URL'],
        MessageBody=json.dumps(event)
    )
