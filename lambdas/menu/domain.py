class Menu:

    def __init__(self, **kwargs):
        self.merchant_id = kwargs["merchantId"]
        self.name = kwargs["name"]
        self.products = []
        self.categories = []

    def add_category(self, name):
        category = Category(name)
        self.categories.append(category)
        return category

    def add_product(self, product):
        self.products.append(product)


class Category:

    def __init__(self, name):
        self.name = name


class Product:

    def __init__(self, **kwargs):
        self.description = kwargs["description"]
        self.price = kwargs["price"]
        self.category = kwargs["category"]