import boto3
from domain import Menu, MenuItem


class MenuRepository:

    def __init__(self):
        self._dynamodb = boto3.resource("dynamodb")
        self._table = self._dynamodb.Table("bohr-menu")

    def save(self, menu: Menu):
        db_item = serialize_menu(menu)
        db_item["pk"] = f"MERCHANT#{menu.merchant_id}"

        self._table.put_item(
            Item=db_item
        )


def serialize_menu(menu: Menu):
    return {
        "merchant_id": menu.merchant_id,
        "name": menu.name,
        "items": [serialize_menu_item(menuItem) for menuItem in menu.items],
        "status": menu.status,
        "date_created": menu.date_created
    }


def serialize_menu_item(menuItem: MenuItem):
    return {
        "description": menuItem.description,
        "category": menuItem.category,
        "price": menuItem.price
    }
