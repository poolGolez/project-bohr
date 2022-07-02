from domain import Menu, MenuItem


def marshal_menu(menu: Menu):
    return {
        "id": menu.id,
        "merchant_id": menu.merchant_id,
        "name": menu.name,
        "items": [marshal_menu_item(menuItem) for menuItem in menu.items],
        "status": menu.status,
        "date_created": menu.date_created.strftime("%Y-%m-%d %H:%M:%S")
    }


def marshal_menu_metadata(menu: Menu):
    return {
        "id": menu.id,
        "merchant_id": menu.merchant_id,
        "name": menu.name,
        "status": menu.status,
        "date_created": menu.date_created.strftime("%Y-%m-%d %H:%M:%S")
    }


def marshal_menu_item(menu_item: MenuItem):
    return {
        "description": menu_item.description,
        "category": menu_item.category,
        "price": float(menu_item.price)
    }
