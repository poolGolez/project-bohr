import boto3
import json
from datetime import datetime
from request import RequestMenuMapper


dynamodb = boto3.resource("dynamodb")
menu_table = dynamodb.Table("bohr-menu")
request_mapper = RequestMenuMapper()


def handler(event, context):
    merchant_id = event["pathParameters"]["merchantId"]
    request_body = json.loads(event['body'])

    menu = request_mapper.map(event)
    # content = request_body["items"]
    now = datetime.now()

    menu_table.put_item(
        Item={
            "pk": f"MECHANT#{menu.merchant_id}",
            "merchant_id": menu.merchant_id,
            "name": menu.name,
            # "content": content,
            "status": "ACTIVE",
            "date_created": now.strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    return {
        "statusCode": "200",
        "headers": {
            "Content-type": "application/json"
        },
        "body": json.dumps({
            "merchantId": merchant_id,
            # "content": content
        })
    }
