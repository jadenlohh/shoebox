import uuid
import enum
import shelve
from flask import session


class UserRole(enum.IntEnum):
    admin = 0
    customer = 1


class User:
    def __init__(self, firstName: str, lastName: str, email: str, password: str, role: UserRole, cart = []):
        self.id = str(uuid.uuid4())
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.role = role
        self.cart = cart
        self.postalCode = ''
        self.address = ''
        self.unitNumber = ''

    def get_id(self):
        return self.id

    def get_firstName(self):
        return self.firstName

    def get_lastName(self):
        return self.lastName

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role

    def get_cart(self) -> list:
        return self.cart
        
    def get_unitNumber(self):
        return self.unitNumber

    def get_address(self):
        return self.address

    def get_postalCode(self):
        return self.postalCode

    def set_firstname(self, firstName):
        self.firstName = firstName

    def set_lastName(self, lastName):
        self.lastName = lastName

    def set_password(self, password):
        self.password = password

    def set_email(self, email):
        self.email = email

    def set_cart(self, cart):
        self.cart = cart

    def set_unitNumber(self, unitNumber):
        self.unitNumber = unitNumber

    def set_address(self, address):
        self.address = address

    def set_postalCode(self, postalCode):
        self.postalCode = postalCode


def get_all_users():
    with shelve.open('./database/data') as db:
        return db.get('users', {})


def save_to_db(userID, user):
    with shelve.open('./database/data') as db:
        table = get_all_users()

        table[userID] = user
        db['users'] = table


class Users:

    @staticmethod
    def register(user: User) -> User:
        table = get_all_users()

        if not user.get_id() in table:
            save_to_db(user.get_id(), user)

            return user

        else:
            raise KeyError


    @staticmethod
    def update(id, user: User) -> User:
        table = get_all_users()

        if not id in table:
            raise KeyError
            
        else:
            save_to_db(id, user)

            return user


    @staticmethod
    def list() -> list:
        table = get_all_users()
        return table.values()


    @staticmethod
    def select_email(email: str) -> User:
        users = Users.list()

        for u in users:
            if u.get_email() == email:
                return u

        return None


    @staticmethod
    def select(id: str) -> User:
        table = get_all_users()

        if id in table:
            return table[id]

        else:
            raise KeyError


    @staticmethod
    def delete(id) -> User:
        with shelve.open('./database/data') as db:
            table = db.get('users', {})
            
            if id in table:
                del table[id]
                db['users'] = table

            else:
                raise KeyError


    @staticmethod
    def get_cart(id) -> User:
        user = Users.select(id)
        total_items = 0

        for x in user.get_cart():
            total_items += x['quantity']

        session['totalItems'] = total_items
        return user.get_cart()    


    @staticmethod
    def update_cart(id, itemID, action) -> User:
        table = get_all_users()

        if id in table:
            user = Users.select(id)
            cart = user.get_cart()

            if cart == []:
                cart.append({'itemID': itemID, 'quantity': 1})

            else:
                item_number = 0
                changed_cart = False

                for item in cart:
                    if (item['itemID'] == itemID) and (action == 'add'):
                        cart[item_number] = {'itemID': itemID, 'quantity': item['quantity'] + 1}
                        changed_cart = True

                    elif (item['itemID'] == itemID) and (action == 'delete'):
                        if item['quantity'] == 1:
                            cart.pop(item_number)
                            changed_cart = True

                        else:
                            cart[item_number] = {'itemID': itemID, 'quantity': item['quantity'] - 1}
                            changed_cart = True

                    item_number += 1

                if not changed_cart:
                    cart.append({'itemID': itemID, 'quantity': 1})

            total_items = 0

            for x in cart:
                total_items += x['quantity']

            session['totalItems'] = total_items
            save_to_db(id, user)

            return user.get_cart()

        else:
            raise KeyError
