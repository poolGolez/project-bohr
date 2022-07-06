from datetime import datetime
from domain import Menu, MenuItem

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
