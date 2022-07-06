from domain import Menu
from repository import deserialize_menu_metadata, serialize_menu_metadata
from marshaller import marshal_menu_metadata
from request import http_response_ok
import boto3


DB_TABLE_NAME = "bohr-menu"

table = boto3.resource("dynamodb").Table(DB_TABLE_NAME)


@http_response_ok
def handler(event, _):
    merchant_id = event["pathParameters"]["merchantId"]
    menu_id = event["pathParameters"]["menuId"]

    menu: Menu = activate_menu(merchant_id, menu_id)

    return marshal_menu_metadata(menu)


def activate_menu(merchant_id: str, target_menu_id: str) -> Menu:
    menus = find_all_by_merchant_id(merchant_id)

    target_menu = None
    for menu in menus:
        if menu.id == target_menu_id:
            menu.activate()
            target_menu = menu
        else:
            menu.deactivate()

    batch_save_metadata(menus)
    return target_menu


def find_all_by_merchant_id(merchant_id: str) -> list:
    results = table.query(
        KeyConditionExpression="#pk = :pk",
        ExpressionAttributeNames={
            "#pk": "pk"
        },
        ExpressionAttributeValues={
            ":pk": f"MERCHANT#{merchant_id}"
        }
    )
    return [deserialize_menu_metadata(item) for item in results["Items"]]


def batch_save_metadata(menus: list):
    with table.batch_writer() as batch:
        for menu in menus:
            batch.put_item(Item=serialize_menu_metadata(menu))
