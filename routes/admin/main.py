from flask import Blueprint, session, redirect, render_template, request
from data.products import Products
from data.user import *
from data.order import *
from routes.admin.customers import router as manageCustomers
from routes.admin.product import router as manageProducts
from routes.admin.orders import router as manageOrders

router = Blueprint('admin', __name__, url_prefix='/admin')

router.register_blueprint(manageCustomers)
router.register_blueprint(manageProducts)
router.register_blueprint(manageOrders)


@router.before_request
def check_authorised():
    if session.get('authenticated') != 'true':
        return redirect('/admin/login?redirect=' + request.path)

    else:
        return None


@router.get('/')
def redirect_to_dashboard():
    return redirect('/admin/dashboard')


@router.get('/dashboard')
def dashboard():
    total_users = 0
    total_sales = 0
    total_orders = 0
    orders = []

    for user in Users.list():
        if user.get_role() == UserRole.customer:
            total_users += 1

    for order in Orders.list():
        x = { 'order': order, 'items': [] }

        for i in order.get_products():
            x['items'].append(Products.select(i['itemID']).get_name())

        orders.append(x)
        total_sales += order.get_amount()
        total_orders += 1

    return render_template('admin/dashboard.html', totalUsers=total_users, totalSales = total_sales, totalOrders = total_orders, orders=reversed(orders[:8]))
