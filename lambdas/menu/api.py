import json
from re import I
from marshaller import marshal_menu, marshal_menu_metadata
from repository import MenuRepository
from request import MenuMapper, http_response_ok
from uuid import uuid4
from datetime import datetime


request_mapper = MenuMapper()
repository = MenuRepository()


@http_response_ok
def create(event, context):
    request_body = dict(json.loads(event['body']))
    request_body["merchant_id"] = event["pathParameters"]["merchantId"]

    menu = request_mapper.map(request_body)
    menu.id = str(uuid4())[-6:]
    menu.status = "ACTIVE"
    menu.date_created = datetime.now()
    repository.save(menu)

    return marshal_menu(menu)


@http_response_ok
def list(event, context):
    merchant_id = event["pathParameters"]["merchantId"]
    menus = repository.find_all_by_merchant_id(merchant_id)

    return [marshal_menu_metadata(menu) for menu in menus]


@http_response_ok
def get(event, context):
    merchant_id = event["pathParameters"]["merchantId"]
    menu_id = event["pathParameters"]["menuId"]
    menu = repository.find_by_merchant_and_menu(merchant_id, menu_id)

    if(menu is None):
        return None

    return marshal_menu(menu)
