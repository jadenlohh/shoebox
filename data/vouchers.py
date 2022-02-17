import uuid
import shelve


class Voucher:
    def __init__(self, name: str, amount: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.amount = amount


    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def set_name(self, name):
        self.name = name

    def set_amount(self, amount):
        self.amount = amount


class Vouchers:

    @staticmethod
    def add(voucher: Voucher) -> Voucher:
        with shelve.open('./database/data') as db:
            table = db.get('vouchers', {})

            if not voucher.get_id() in table:
                table[voucher.get_id()] = voucher
                db['vouchers'] = table
                return voucher
            else:
                raise KeyError

    @staticmethod
    def update(id, voucher: Voucher) -> Voucher:
        with shelve.open('./database/data') as db:
            table = db.get('vouchers', {})

            if not id in table:
                raise KeyError

            else:
                table[id] = voucher
                db['vouchers'] = table

                return voucher

    @staticmethod
    def list() -> list:
        with shelve.open('./database/data') as db:
            table = db.get('vouchers', {})
            return table.values()

    @staticmethod
    def select(id: str) -> Voucher:
        with shelve.open('./database/data') as db:
            table = db.get('vouchers', {})

            if id in table:
                return table[id]

            else:
                raise KeyError

    @staticmethod
    def delete(id) -> Voucher:
        with shelve.open('./database/data') as db:
            table = db.get('vouchers', {})

            if id in table:
                del table[id]
                db['vouchers'] = table

            else:
                raise KeyError
