import json
from marshaller import marshal_menu
from repository import MenuRepository
from request import MenuMapper, http_response_ok


request_mapper = MenuMapper()
repository = MenuRepository()


@http_response_ok
def handler(event, context):
    request_body = dict(json.loads(event['body']))
    request_body["merchant_id"] = event["pathParameters"]["merchantId"]

    menu = request_mapper.map(request_body)
    repository.save(menu)

    return marshal_menu(menu)
