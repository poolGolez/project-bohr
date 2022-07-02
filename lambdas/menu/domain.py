from decimal import Decimal
from datetime import datetime
from uuid import uuid4


class MenuItem:

    def __init__(self, **kwargs):
        self.description = kwargs["description"]
        self.price = Decimal(kwargs["price"])
        self.category = kwargs["category"]


class Menu:

    def __init__(self, **kwargs):
        self.id = str(uuid4())[-6:]
        self.merchant_id = kwargs["merchant_id"]
        self.name = kwargs["name"]
        self.items = []
        self.categories = []
        self.status = "ACTIVE"
        self.date_created = datetime.now()

    def add_menu_item(self, menu_item: MenuItem):
        self.items.append(menu_item)
