from domain import Menu, MenuItem


class MenuMapper:

    def map(self, request_body):
        menu = Menu(
            merchantId=request_body["merchant_id"],
            name=request_body["merchant_id"]
        )

        content = request_body["items"]
        self._add_items(menu, content)

        return menu

    def _add_items(self, menu:Menu, items):
        for item_json in items:
            menu_item = MenuItem(
                description=item_json["description"],
                price= item_json["price"],
                category=item_json["category"]
            )
            menu.add_menu_item(menu_item)
