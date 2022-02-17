from flask import Blueprint, jsonify, render_template, session, request, redirect
from data.products import Products
from data.user import *
from data.order import *
import hashlib

router = Blueprint('profile', __name__, template_folder='./templates')


@router.before_request
def check_loggedIn():
    if session.get('userid') is None:
        return redirect('/login?redirect=/account')

    else:
        return None 


@router.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user = Users.select(session['userid'])

        user.set_firstname(request.form.get('firstName'))
        user.set_lastName(request.form.get('lastName'))
        user.set_email(request.form.get('email'))

        session['firstName'] = request.form.get('firstName')

        Users.update(session['userid'], user)
        return render_template('/customer/profile/account.html', profile=Users.select(session['userid']), success=True)

    else:
        return render_template('/customer/profile/account.html', profile=Users.select(session['userid']))


@router.route('/account/change-pwd', methods=['GET', 'POST'])
def change_pwd():
    if request.method == 'POST':
        user = Users.select(session['userid'])
        currentPwd = hashlib.sha256(request.form.get('currentPwd').encode()).hexdigest()
        newPwd = hashlib.sha256(request.form.get('newPwd').encode()).hexdigest()

        if currentPwd == user.get_password():
            user.set_password(newPwd)
            Users.update(session['userid'], user)

            return redirect('/account/change-pwd')

        else:
           return render_template('/customer/profile/change-pwd.html', profile=Users.select(session['userid']), err='incorrectPwd')

    else:
        return render_template('/customer/profile/change-pwd.html', profile=Users.select(session['userid']))


@router.route('/account/address', methods=['GET', 'POST'])
def manage_address():
    if request.method == 'POST':
        user = Users.select(session['userid'])

        user.set_address(request.form.get('address'))
        user.set_unitNumber(request.form.get('unitNumber'))
        user.set_postalCode(request.form.get('postalCode'))


        Users.update(session['userid'], user)
        return render_template('/customer/profile/manage-address.html', profile=Users.select(session['userid']), success=True)

    else:
        return render_template('/customer/profile/manage-address.html', profile=Users.select(session['userid']))


@router.get('/account/orders')
def view_orders():
    orders = []

    for order in Orders.list():
        if order.get_customerID() != session['userid']:
            continue

        order_details = {}
        items = []

        for item in order.get_products():
            itemClass = Products.select(item.get('itemID'))

            item_details = {
                'name': itemClass.get_name(),
                'image': itemClass.get_image(),
                'category': itemClass.get_category(),
                'price': itemClass.get_price(),
                'quantity': item.get('quantity')
            }

            items.append(item_details)

        order_details['items'] = items
        order_details['orderID'] = order.get_id()
        order_details['status'] = order.get_status()
        order_details['total'] = order.get_amount()
        orders.append(order_details)

    return render_template('/customer/profile/manage-order.html', profile=Users.select(session['userid']), orders=reversed(orders))


@router.get('/account/orders/reorder/<id>')
def reorder(id):
    for order in Orders.list():
        if order.get_id() != id:
            continue

        for i in order.get_products():
            Users.update_cart(session['userid'], i['itemID'], 'add')

        session['totalItems'] = len(order.get_products())

    return redirect('/cart')