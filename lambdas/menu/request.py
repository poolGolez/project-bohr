import json
from domain import Menu, MenuItem


class MenuMapper:

    def map(self, request_body):
        menu = Menu(
            merchant_id=request_body["merchant_id"],
            name=request_body["name"]
        )

        content = request_body["items"]
        self._add_items(menu, content)

        return menu

    def _add_items(self, menu: Menu, items):
        for item_json in items:
            menu_item = MenuItem(
                description=item_json["description"],
                price=item_json["price"],
                category=item_json["category"]
            )
            menu.add_menu_item(menu_item)


def http_response_ok(handler):
    def wrapper(event, context):
        return {
            "statusCode": "200",
            "headers": {
                "Content-type": "application/json"
            },
            "body": json.dumps(handler(event, context))
        }

    return wrapper
