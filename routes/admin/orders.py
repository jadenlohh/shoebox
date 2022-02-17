from flask import Blueprint, render_template, request, redirect, jsonify
from data.order import *
from data.products import *

router = Blueprint('adminOrders', __name__, url_prefix='/orders', template_folder='./templates')


def form_input(item):
    return request.form.get(item)


@router.get('')
def manage_orders():
    return render_template('admin/manage-orders/orders.html')


@router.get('/retrive')
def get_all_orders():
    orders = []

    for i in Orders.list():
        products = []

        for product in i.get_products():
            products.append(f"{product['quantity']} x {Products.select(product['itemID']).get_name()}")
        
        productName = ', '.join(products)

        x = {
            'id': i.get_id(),
            'customerName': i.get_customerName(),
            'products': productName,
            'amount': i.get_amount(),
            'address': i.get_address(),
            'postalCode': i.get_postalCode(),
            'status': i.get_status()
        }
        orders.append(x)

    return jsonify(orders)



@router.get('/update/<id>')
def edit_details(id):

    orderDatail = []
    order=Orders.select(id) # Select order ID
    productID = order.get_products() # Get order item

    for item in productID:
        x = {}

        itemDetail = item.get("itemID")
        itemqty = item.get("quantity")
        detail = Products.select(itemDetail)
        x['qty'] = itemqty
        x['product'] = detail

        orderDatail.append(x)

    return render_template('admin/manage-orders/edit.html', products= orderDatail, order= order)




@router.post('/update/<id>')
def update_details(id):
    try:
        order = Orders.select(id)        
        order.set_status('To Ship')
        Orders.update(id, order)

        orderDatail = []
        order=Orders.select(id) # Select order ID
        productID = order.get_products() # Get order item

        for item in productID:
            x = {}

            itemDetail = item.get("itemID")
            itemqty = item.get("quantity")
            detail = Products.select(itemDetail)
            x['qty'] = itemqty
            x['product'] = detail

            orderDatail.append(x)

        return render_template('admin/manage-orders/edit.html', success=True, order=order, products= orderDatail)

    except KeyError:
        return redirect('/admin/orders')



@router.get('/delete/<id>')
def delete_order(id):
    try:
        Orders.delete(id)
        
        return redirect('/admin/orders')

    except KeyError:
        return redirect('/admin/orders')
