import json

def handler(event, context):
    print("Processing message:", json.dumps(event))
