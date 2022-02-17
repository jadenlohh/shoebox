from flask import Blueprint, render_template, redirect, request, jsonify
from data.vouchers import *

router = Blueprint('adminVouchers', __name__, url_prefix='/voucher', template_folder='./templates')


def form_input(item):
    return request.form.get(item)


@router.get('/')
def manage_vouchers():
    return render_template('admin/manage-vouchers/vouchers.html', vouchers=Vouchers.list())


@router.get('/retrive')
def get_all_vouchers():
    vouchers = []

    for i in Vouchers.list():
        x = {
            'id': i.get_id(),
            'name': i.get_name(),
            'description': i.get_amount(),
        }
        vouchers.append(x)

    r = jsonify(vouchers)
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "X-Requested-With"

    return r


@router.route('/create', methods=['GET', 'POST'])
def create_voucher():
    if request.method == 'POST':
        voucher = Voucher(form_input('name'), form_input('amount'))

        Vouchers.add(voucher)

        return render_template('admin/manage-products/create.html', success=True)

    else:
        return render_template('admin/manage-vouchers/create.html')


@router.route('/update/<id>', methods=['GET', 'POST'])
def update_details(id):
    if request.method == 'POST':
        voucher = Vouchers.select(id)

        voucher.set_name(form_input('name'))
        voucher.set_amount(form_input('description'))

        Vouchers.update(id, voucher)
        return render_template('admin/manage-vouchers/update.html', success=True, voucher=Vouchers.select(id))

    else:
        return render_template('admin/manage-vouchers/update.html', voucher=Vouchers.select(id))


@router.get('/delete/<id>')
def delete_product(id):
    try:
        Vouchers.delete(id)

        return redirect('/admin/products')

    except KeyError:
        return redirect('/admin/products')
