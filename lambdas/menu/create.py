import json

def handler(event, context):
    merchant_id = event["pathParameters"]["merchantId"]
    request_body = json.loads(event['body'])

    return {
        "statusCode": "200",
        "headers": {
            "Content-type": "application/json"
        },
        "body": json.dumps({
            "merchantId": merchant_id,
            "body": request_body
        })
    }
