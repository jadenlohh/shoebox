from flask import Blueprint, jsonify, render_template, request, session, redirect
from data.user import *
from data.products import *
from data.order import *
import hashlib, base64
import datetime
import json
import urllib.parse

router = Blueprint('payment', __name__, url_prefix="/payment", template_folder='./templates')

api_secret_key = '38a4b473-0295-439d-92e1-ad26a8c60279'
api_key = '154eb31c-0f72-45bb-9249-84a1036fd1ca'


def txnRequest(amount, method, refDate, transDate):
    with open('./data/query.json', 'r') as j:
        data = json.load(j)
        data['msg']['txnAmount'] = str(amount)
        data['msg']['merchantTxnRef'] = refDate
        data['msg']['merchantTxnDtm'] = transDate
        data['msg']['paymentMode'] = method
        
        return json.dumps(data, sort_keys=False)


def generate_MAC_value(payload):
    content = str(payload) + api_secret_key
    m = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return base64.b64encode(bytes.fromhex(m)).decode("utf-8")


@router.before_request
def check_loggedIn():
    if session.get('userid') is None:
        return redirect('/login?redirect=/cart')

    else:
        return None 


@router.get('')
def payment():
    try:
        paymentType = request.args.get('type')
        date = datetime.datetime.now()
        amount = int(session['totalCartAmount']) * 100

        payload = str(txnRequest(amount, paymentType, date.strftime('%Y%m%d %I:%M:%S'), date.strftime('%Y%m%d %I:%M:%S.%f')[:-3]))
        MAC_value = generate_MAC_value(payload)

        return render_template('/customer/payments/payment.html', txnReq=payload, keyID=api_key, MAC_value=MAC_value)
    
    except KeyError:
        return redirect('/cart')


@router.route('/complete', methods=['GET', 'POST'])
def payment_completed():
    if request.method == 'GET':
        return redirect('/cart')
    
    else:
        message = json.loads(urllib.parse.unquote(request.form.get('message')))
        
        try:
            if message['msg']['netsTxnStatus'] == '0':
                order = Order(Users.get_cart(session['userid']), session['orderDetails']['name'], 
                session['orderDetails']['address'], session['orderDetails']['postalCode'], session['orderDetails']['unitNumber'],
                session['totalCartAmount'])

                order.set_customerID(session['userid'])
                Orders.create(order)

                for i in Users.get_cart(session['userid']):
                    Products.remove_stock(i.get('itemID'), i.get('quantity'))
                    Products.add_sales(i.get('itemID'),  i.get('quantity'))
                    Users.update_cart(session['userid'], i.get('itemID'), 'delete')

                session['cartItems'] = 0
                return render_template('/customer/payments/success.html')

            elif message['msg']['netsTxnStatus'] == '9':
                return redirect('/cart')

            else:
                return redirect('/payment/error')

        except:
            return redirect('/payment/error')


@router.route('/error')
def payment_error():
    msg = "Oh no! Your payment was unsuccessful but dont't worry, you will be redirected back to your cart in 5 seconds"
    return render_template('/error.html', error_type='Payment Error', error_msg=msg)
