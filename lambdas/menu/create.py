import json
from marshaller import marshal_menu
from repository import MenuRepository
from request import MenuMapper


request_mapper = MenuMapper()
repository = MenuRepository()


def handler(event, context):
    request_body = dict(json.loads(event['body']))
    request_body["merchant_id"] = event["pathParameters"]["merchantId"]

    menu = request_mapper.map(request_body)
    repository.save(menu)

    return {
        "statusCode": "201",
        "headers": {
            "Content-type": "application/json"
        },
        "body": json.dumps(marshal_menu(menu))
    }
