from flask import Blueprint, render_template, session, request, redirect, url_for, make_response
from data.user import *
from data.products import *

router = Blueprint('cart', __name__, url_prefix='/cart', template_folder='./templates')


@router.before_request
def check_loggedIn():
    if session.get('userid') is None:
        return redirect('/login?redirect=/cart')

    else:
        return None 


@router.get('')
def cart():
    redirectUrl = request.args.get('next')
    cart = Users.get_cart(session['userid'])

    if cart != []:
        item_details = []
        subtotal = 0
        items = 0

        for i in cart:
            item = Products.select(i.get('itemID'))

            x = {
                'id': item.get_id(),
                'image': item.get_image(),
                'name': item.get_name(),
                'category': item.get_category(),
                'price': f'{item.get_price()}.00',
                'quantity': i.get('quantity')
            }

            item_details.append(x)
            subtotal += (int(item.get_price()) * int(i.get('quantity')))
            items += int(i.get('quantity'))

        session['subtotal'] = subtotal
        session['totalCartAmount'] = subtotal + 4
        session['totalItems'] = items

        item_details.append({'subtotal': subtotal, 'deliveryFee': 4, 'total': subtotal + 4})

        if redirectUrl:
            return redirect(redirectUrl)

        return render_template('customer/cart.html', items=item_details)

    session['totalItems'] = 0
    return render_template('customer/cart.html', items=[{'subtotal': 0, 'deliveryFee': 0,'total': 0}])


@router.get('/get-discountCodes')
def get_discounts():
    code = request.args.get('code').upper()

    if code == 'NEWYEAR50':
        session['totalCartAmount'] -= 50
        return {'valid': True, 'amount': 50, 'totalCartAmount': session['totalCartAmount']}

    else:
        return {'valid': False}


@router.get('/add/<id>')
def add_to_cart(id):
    sourceURL = request.args.get('source')
    nextURL = request.args.get('next')
    Users.update_cart(session['userid'], id, 'add')

    if session['totalItems'] != 0:
        i = session['totalItems'] + 1
        session['totalItems'] = i

    else:
        session['totalItems'] = 1


    if sourceURL and nextURL:
        r = redirect(sourceURL + '?next=' + nextURL)

    elif sourceURL:
        r = redirect(sourceURL)
        r.set_cookie('addToCart', 'successful', max_age=3)

    else:
        r = redirect('/cart')

    return r


@router.get('/delete/<id>')
def remove_from_cart(id):
    Users.update_cart(session['userid'], id, 'delete')
    session['totalItems'] - 1

    return redirect('/cart')


@router.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart = Users.get_cart(session['userid'])
        cart_items = []
        
        for i in cart:
            cart_items.append({'item': Products.select(i.get('itemID')), 'qty': i.get('quantity')})

        if request.cookies.get('discount') is None:
            return render_template('/customer/payments/form.html', cart=cart_items, user=Users.select(session['userid']))

        resp = make_response(render_template('/customer/payments/form.html', cart=cart_items, user=Users.select(session['userid']), discount=request.cookies.get('discount')))
        resp.set_cookie('discount', '', max_age=0)
        return resp

    else:
        session['orderDetails'] = {
            'name': f"{request.form.get('firstName')} {request.form.get('lastName')}",
            'address': request.form.get('address'),
            'postalCode': request.form.get('postalCode'),
            'unitNumber': request.form.get('unitNumber')
        }

        if request.form.get('saveInformation'):
            user = Users.select(session['userid'])
            user.set_address(request.form.get('address'))
            user.set_postalCode(request.form.get('postalCode'))
            user.set_unitNumber(request.form.get('unitNumber'))

            Users.update(session['userid'], user)

        if request.form.get('paymentType') == 'creditCard':
            return redirect(url_for('customer.payment.payment', type='CC'))

        else:
            return redirect(url_for('customer.payment.payment', type='QR'))
