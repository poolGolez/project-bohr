from decimal import Decimal
from datetime import datetime


class MenuItem:

    def __init__(self, **kwargs):
        self.description = kwargs["description"]
        self.price = Decimal(kwargs["price"])
        self.category = kwargs["category"]

class Menu:

    def __init__(self, **kwargs):
        self.merchant_id = kwargs["merchantId"]
        self.name = kwargs["name"]
        self.items = []
        self.categories = []
        self.status = "ACTIVE"
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_menu_item(self, menu_item: MenuItem):
        self.items.append(menu_item)
