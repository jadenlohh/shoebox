from flask import Blueprint, render_template, request, redirect, session
import hashlib
from data.user import *
import sendgrid
from sendgrid.helpers.mail import Mail
import jwt
import datetime

router = Blueprint('auth', __name__, template_folder='./templates')


def form_input(item):
    return request.form.get(item)

def session_login(user):
    session['userid'] = user.get_id()
    session['firstName'] = user.get_firstName()
    numOfItem = 0

    for i in user.get_cart():
        i['quantity'] += numOfItem

    session['totalItems'] = numOfItem


@router.get('/login')
def login_page():
    return render_template('customer/auth/login.html', error=None)


@router.get('/register')
def register_page():
    return render_template('customer/auth/registration.html', error=None)


@router.post('/login')
def login_user():
    redirectURL = request.args.get('redirect')
    sourceURL = request.args.get('source')
    
    user = Users.select_email(form_input('email'))
    hash_pwd = hashlib.sha256(form_input('password').encode()).hexdigest()

    if user is not None:
        if user.get_password() == hash_pwd:
            session_login(user)

            if redirectURL:
                newURL = redirectURL + '?source=' + sourceURL if sourceURL is not None else redirectURL
                return redirect(newURL)
            
            return redirect('/')

    return render_template('customer/auth/login.html', error='Invalid email or password')


@router.post('/register')
def register_user():
    for u in Users.list():
        if u.get_email() == form_input('email'):
            return render_template('customer/auth/registration.html', error='Email already registered')

    hash_pwd = hashlib.sha256(form_input('password').encode()).hexdigest()

    user = User(form_input('firstName'), form_input('lastName'), form_input('email'), hash_pwd, UserRole.customer)
    Users.register(user)
        
    session_login(user)
    return redirect('/')


@router.get('/logout')
def logout():
    session.pop('userid')
    return redirect('/')


@router.route('/forget-password', methods=['GET', 'POST'])
def forgetPwd():
    if request.method == 'GET':
        return render_template('customer/forgot-pwd/reset-form.html')

    email = request.form.get('email')
    time = datetime.datetime.now() + datetime.timedelta(minutes=10)
    code = jwt.encode({"email": email, 'expiry': time.strftime('%d %b %Y %H:%M:%S')}, "My3upErSecr3tKe#", algorithm="HS256")

    message = Mail(
        from_email='sh03b0x.help@gmail.com',
        to_emails=email,
        subject='Reset Password',
        html_content=render_template('customer/forgot-pwd/email_template.html', code=code)
    )

    sg = sendgrid.SendGridAPIClient('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')
    sg.send(message)

    return {'success': True}
    

@router.route('/verify/<code>', methods=['GET', 'POST'])
def verify_email(code):
    if request.method == 'GET':
        payload = jwt.decode(code, "My3upErSecr3tKe#", algorithms=["HS256"])
        time = datetime.datetime.now()

        if datetime.datetime.now() > time.strptime(payload['expiry'], '%d %b %Y %H:%M:%S'):
            return render_template('customer/forgot-pwd/reset-pwd.html', error='Time expired')

        return render_template('customer/forgot-pwd/reset-pwd.html', email=payload.get('email'))

    else:
        password = request.form.get('password')
        hash_pwd = hashlib.sha256(password.encode()).hexdigest()

        user = Users.select_email(request.form.get('email'))
        user.set_password(hash_pwd)
        Users.update(user.get_id(), user)

        session_login(user)
        return redirect('/')