from datetime import datetime
from time import strptime
import boto3
from uuid import uuid4
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

    def find_by_merchant_and_menu(self, merchant_id, menu_id):
        results = self._dynamodb.batch_get_item(
            RequestItems={
                DB_TABLE_NAME: {
                    "Keys": [
                        {
                            "pk": f"MERCHANT#{merchant_id}",
                            "sk": f"MENU#{menu_id}"
                        },
                        {
                            "pk": f"MENU#{menu_id}",
                            "sk": f"MENU#{menu_id}"
                        }
                    ]
                }
            }
        )

        metadata = [item for item in results["Responses"][DB_TABLE_NAME]
                    if item["pk"] == f"MERCHANT#{merchant_id}"][0]
        content = [item for item in results["Responses"][DB_TABLE_NAME]
                   if item["pk"] == f"MENU#{menu_id}"][0]["content"]

        return deserialize_menu(metadata, content)

    def save(self, menu: Menu):
        menu.id = str(uuid4())[-6:]
        menu.status = "ACTIVE"
        menu.date_created = datetime.now()

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


def deserialize_menu_metadata(metadata):
    return Menu(
        id=metadata["id"],
        merchant_id=metadata["merchant_id"],
        name=metadata["name"],
        status=metadata["status"],
        date_created=datetime.strptime(
            metadata["date_created"], "%Y-%m-%d %H:%M:%S")
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


def deserialize_menu(metadata, items=[]):
    menu = deserialize_menu_metadata(metadata)
    menu.items = [deserialize_menu_item(item) for item in items]

    return menu


def deserialize_menu_item(item):
    return MenuItem(
        description=item["description"],
        price=item["price"],
        category=item["category"]
    )
