from decimal import Decimal
from datetime import datetime


class MenuItem:

    def __init__(self, **kwargs):
        self.description = kwargs["description"]
        self.price = Decimal(kwargs["price"])
        self.category = kwargs["category"]


class Menu:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.merchant_id = kwargs.get("merchant_id", None)
        self.name = kwargs.get("name", None)
        self.items = kwargs.get("items", [])
        self.status = kwargs.get("status", None)
        self.date_created = kwargs.get("date_created", None)

    def add_menu_item(self, menu_item: MenuItem):
        self.items.append(menu_item)
