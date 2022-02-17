import uuid
import shelve
import datetime


class Order:
    def __init__(self, products: dict, customerName: str, address: str, postalCode: str, unitNumber: str, amount: str, status='Paid'):
        id = str(uuid.uuid4()).split("-")
        self.id = f'{id[0]}-{id[1]}'

        self.products = products
        self.customerID = None
        self.customerName = customerName
        self.address = address
        self.postalCode = postalCode
        self.unitNumber = unitNumber
        self.amount = amount
        self.status = status

        x = datetime.datetime.now()
        self.purchaseDate = x.strftime('%d/%m/%Y %I:%M:%S%p')

    def get_id(self):
        return self.id

    def get_products(self):
        return self.products

    def get_customerID(self):
        return self.customerID

    def get_customerName(self):
        return self.customerName

    def get_address(self):
        return self.address

    def get_postalCode(self):
        return self.postalCode

    def get_unitNumber(self):
        return self.unitNumber

    def get_amount(self):
        return self.amount

    def get_status(self):
        return self.status

    def get_purchaseDate(self):
        return self.purchaseDate  


    def set_products(self, products):
        self.products = products

    def set_customerID(self, id):
        self.customerID = id

    def set_customerName(self, customerName):
        self.customerName = customerName

    def set_address(self, address):
        self.address = address

    def set_postalCode(self, postalCode):
        self.postalCode = postalCode

    def set_unitNumber(self, unitNumber):
        self.unitNumber = unitNumber

    def set_amount(self, amount):
        self.amount = amount

    def set_status(self, status):
        self.status = status


def get_all_orders():
    with shelve.open('./database/data') as db:
        return db.get('orders', {})


def save_to_db(orderID, order):
    with shelve.open('./database/data') as db:
        table = get_all_orders()

        table[orderID] = order
        db['orders'] = table


class Orders:

    @staticmethod
    def create(order: Order) -> Order:
        table = get_all_orders()

        if not order.get_id() in table:
            save_to_db(order.get_id(), order)

            return order

        else:
            raise KeyError


    @staticmethod
    def update(id, order: Order) -> Order:
        table = get_all_orders()

        if not id in table:
            raise KeyError
            
        else:
            save_to_db(id, order)

            return order


    @staticmethod
    def list() -> list:
        table = get_all_orders()
        return table.values()


    @staticmethod
    def select(id: str) -> Order:
        table = get_all_orders()

        if id in table:
            return table[id]

        else:
            raise KeyError


    @staticmethod
    def delete(id) -> Order:
        order = Orders.select(id)
        order.set_status('Cancelled')

        save_to_db(id, order)
        return order
