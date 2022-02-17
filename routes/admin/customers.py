from flask import Blueprint, render_template, request, redirect, jsonify
from data.user import *

router = Blueprint('adminAuth', __name__, url_prefix='/customers', template_folder='./templates')


def form_input(item):
    return request.form.get(item)


@router.get('')
def manage_customers():
    return render_template('admin/manage-customers/customers.html')

    
@router.get('/retrive')
def get_all_users():
    users = []

    for i in Users.list():
        if i.get_role() == UserRole.customer:
            x = {
                'id': i.get_id(),
                'first name': i.get_firstName(),
                'last name': i.get_lastName(),
                'email': i.get_email()
            }
            users.append(x)

    return jsonify(users)


@router.get('/update/<id>')
def edit_details(id):
    return render_template('admin/manage-customers/edit.html', user=Users.select(id))


@router.post('/update/<id>')
def update_details(id):
    try:
        user = Users.select(id)

        user.set_firstname(form_input('firstName'))
        user.set_lastName(form_input('lastName'))

        if form_input('emailChanged') == 'true':
            if Users.select_email(form_input('email')) != None:
                return render_template('admin/manage-customers/edit.html', error='That email already exist', user=Users.select(id)) 

        user.set_email(form_input('email'))

        Users.update(id, user)
        return render_template('admin/manage-customers/edit.html', success=True, user=Users.select(id))

    except KeyError:
        return redirect('/admin/customers')


@router.get('/delete/<id>')
def delete_user(id):
    try:
        Users.delete(id)
        
        return redirect('/admin/customers')

    except KeyError:
        return redirect('/admin/customers')
