from repository import serialize_menu_content, serialize_menu_metadata
from request import http_response_ok
from marshaller import marshal_menu
from domain import Menu, MenuItem

import boto3
import json
from uuid import uuid4
from datetime import datetime

DB_TABLE_NAME = "bohr-menu"
db_table = boto3.resource("dynamodb").Table(DB_TABLE_NAME)


@http_response_ok
def handler(event, _):
    menu: Menu = map_menu_from_event(event)
    menu = create(menu)
    return marshal_menu(menu)


def map_menu_from_event(event) -> Menu:
    request_body = json.loads(event['body'])
    menu = Menu(
        merchant_id=event["pathParameters"]["merchantId"],
        name=request_body["name"]
    )

    for item_json in request_body["items"]:
        menu_item = MenuItem(
            description=item_json["description"],
            price=item_json["price"],
            category=item_json["category"]
        )
        menu.add_menu_item(menu_item)

    return menu


def create(menu: Menu) -> Menu:
    menu.id = str(uuid4())[-6:]
    menu.status = "INACTIVE"
    menu.date_created = datetime.now()

    save(menu)
    return menu


def save(menu: Menu):
    menu_metadata_db_item = serialize_menu_metadata(menu)
    db_table.put_item(Item=menu_metadata_db_item)

    menu_content_db_item = serialize_menu_content(menu)
    db_table.put_item(Item=menu_content_db_item)
