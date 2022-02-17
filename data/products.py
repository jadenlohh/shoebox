import uuid
import shelve


class Product:
    def __init__(self, name: str, description: str, category: str, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.brand = ''
        self.description = description
        self.category = category
        self.price = price
        self.stock = 0
        self.image = ''
        self.totalQtySold = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_brand(self):
        return self.brand

    def get_description(self):
        return self.description

    def get_category(self):
        return self.category

    def get_price(self):
        return self.price

    def get_stock(self):
        return self.stock

    def get_image(self):
        return self.image

    def get_totalQtySold(self):
        return self.totalQtySold

    def set_totalQtySold(self, amount):
        self.totalQtySold = amount

    def set_name(self, name):
        self.name = name

    def set_brand(self, brand):
        self.brand = brand

    def set_description(self, description):
        self.description = description

    def set_category(self, category):
        self.category = category

    def set_price(self, price):
        self.price = int(price)

    def set_stock(self, stock):
        self.stock = int(stock)

    def set_image(self, file):
        self.image = file


def get_all_products():
    with shelve.open('./database/data') as db:
        return db.get('products', {})


def save_to_db(productID, product):
    with shelve.open('./database/data') as db:
        table = get_all_products()

        table[productID] = product
        db['products'] = table


class Products:

    @staticmethod
    def add(product: Product) -> Product:
        table = get_all_products()

        if not product.get_id() in table:
            save_to_db(product.get_id(), product)

            return product

        else:
            raise KeyError


    @staticmethod
    def update(id, product: Product) -> Product:
        table = get_all_products()

        if not id in table:
            raise KeyError
            
        else:
            save_to_db(id, product)

            return product


    @staticmethod
    def list() -> list:
        table = get_all_products()
        return table.values()


    @staticmethod
    def select(id: str) -> Product:
        table = get_all_products()

        if id in table:
            return table[id]

        else:
            raise KeyError


    @staticmethod
    def delete(id) -> Product:
        with shelve.open('./database/data') as db:
            table = db.get('products', {})
            
            if id in table:
                del table[id]
                db['products'] = table

            else:
                raise KeyError
            
    
    @staticmethod
    def remove_stock(id, amount) -> Product:
        item = Products.select(id)
        item.set_stock(int(item.get_stock()) - amount)

        save_to_db(id, item)


    @staticmethod
    def add_sales(id, amount) -> Product:
        item = Products.select(id)
        item.totalQtySold += int(amount)

        save_to_db(id, item)