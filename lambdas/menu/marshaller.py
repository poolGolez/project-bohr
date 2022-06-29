from domain import Menu, MenuItem

def marshal_menu(menu: Menu):
    return {
        "merchant_id": menu.merchant_id,
        "name": menu.name,
        "items": [marshal_menu_item(menuItem) for menuItem in menu.items],
        "status": menu.status,
        "date_created": menu.date_created
    }


def marshal_menu_item(menuItem: MenuItem):
    return {
        "description": menuItem.description,
        "category": menuItem.category,
        "price": float(menuItem.price)
    }
