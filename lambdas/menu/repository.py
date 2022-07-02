import boto3
from domain import Menu, MenuItem

DB_TABLE_NAME = "bohr-menu"


class MenuRepository:

    def __init__(self):
        self._dynamodb = boto3.resource("dynamodb")
        self._table = self._dynamodb.Table(DB_TABLE_NAME)

    def find_all_by_merchant_id(self, merchant_id):
        results = self._table.query(
            KeyConditionExpression="#pk = :pk",
            ExpressionAttributeNames={
                "#pk": "pk"
            },
            ExpressionAttributeValues={
                ":pk": f"MERCHANT#{merchant_id}"
            }
        )
        return [deserialize_menu_metadata(item) for item in results["Items"]]

    def save(self, menu: Menu):
        menu_metadata_db_item = serialize_menu_metadata(menu)
        self._table.put_item(
            Item=menu_metadata_db_item
        )

        menu_content_db_item = serialize_menu_content(menu)
        self._table.put_item(
            Item=menu_content_db_item
        )


def serialize_menu_metadata(menu: Menu):
    return {
        "pk": f"MERCHANT#{menu.merchant_id}",
        "sk": f"MENU#{menu.id}",
        "id": menu.id,
        "merchant_id": menu.merchant_id,
        "name": menu.name,
        "status": menu.status,
        "date_created": menu.date_created.strftime("%Y-%m-%d %H:%M:%S")
    }


def deserialize_menu_metadata(item):
    return Menu(
        merchant_id=item["merchant_id"],
        name=item["name"],
        status=item["status"]
    )


def serialize_menu_content(menu: Menu):
    return {
        "pk": f"MENU#{menu.id}",
        "sk": f"MENU#{menu.id}",
        "content": [serialize_menu_item(item) for item in menu.items]
    }


def serialize_menu_item(menuItem: MenuItem):
    return {
        "description": menuItem.description,
        "category": menuItem.category,
        "price": menuItem.price
    }
