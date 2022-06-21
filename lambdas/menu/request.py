import json
from domain import Menu, Product


class RequestMenuMapper:

    def map(self, event):
        merchant_id = event["pathParameters"]["merchantId"]

        request_body = json.loads(event["body"])
        name = request_body["name"]
        menu = Menu(
            merchantId=merchant_id,
            name=name
        )

        content = request_body["items"]
        self.add_products(menu, content)

        return menu

    def add_products(self, menu, items):
        for item_json in items:
            product = Product(
                description=item_json["description"],
                price= item_json["price"],
                category= item_json["category"]
            )
            menu.add_product(product)
