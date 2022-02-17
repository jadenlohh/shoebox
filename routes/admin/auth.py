from flask import Blueprint, render_template, request, redirect, session
from data.user import *
import hashlib

router = Blueprint('adminAuthentication', __name__, template_folder='./templates', url_prefix='/admin')


def form_input(item):
    return request.form.get(item)


'''
email: admin@gmail.com
password: Password1
'''

@router.get('/login')
def login_page():
    return render_template('admin/login.html', error=None)


@router.post('/login')
def login_user():
    redirectURL = request.args.get('redirect')
    user = Users.select_email(form_input('email'))

    if user is not None:
        hash_pwd = hashlib.sha256(form_input('password').encode()).hexdigest()
        if (user.get_password() == hash_pwd) and (user.get_role() == UserRole.admin):
            session['authenticated'] = 'true'

            if redirectURL:
                return redirect(redirectURL)
            
            return redirect('/admin')

    return render_template('admin/login.html', error='Invalid email or password!')


@router.get('/logout')
def logout():
    session.pop('authenticated')
    return redirect('/admin/login')
