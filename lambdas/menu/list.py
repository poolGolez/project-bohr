from marshaller import marshal_menu_metadata
from request import http_response_ok
from repository import MenuRepository

repository = MenuRepository()


@http_response_ok
def handler(event, context):
    merchant_id = event["pathParameters"]["merchantId"]
    menus = repository.find_all_by_merchant_id(merchant_id)
    return [marshal_menu_metadata(menu) for menu in menus]
