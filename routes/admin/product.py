from flask import Blueprint, render_template, redirect, request
from data.products import *
import os

router = Blueprint('adminProducts', __name__, url_prefix='/products', template_folder='./templates')


def form_input(item):
    return request.form.get(item)


@router.get('')
def manage_products():
    return render_template('admin/manage-products/products.html')


@router.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        product = Product(form_input('name'), form_input('description'), form_input('category'), form_input('price'))
        product.set_brand(form_input('brand'))
        product.set_stock(form_input('stock'))
        
        file = request.files.get('productImage')
        file_type = file.filename.split('.')[1]
        file.save(os.path.join(os.getcwd(), f'public/product-img/{product.get_id()}.{file_type}'))
        product.set_image(f'/public/product-img/{product.get_id()}.{file_type}')

        Products.add(product)
        
        return render_template('admin/manage-products/create.html', success=True)

    else:
        return render_template('admin/manage-products/create.html')


@router.route('/update/<id>', methods=['GET', 'POST'])
def update_details(id):
    if request.method == 'POST':
        try:
            product = Products.select(id)

            product.set_name(form_input('name'))
            product.set_brand(form_input('brand'))
            product.set_description(form_input('description'))
            product.set_category(form_input('category'))
            product.set_price(form_input('price'))
            product.set_stock(form_input('stock'))

            file = request.files.get('productImage')

            if file.filename != '':
                os.unlink(f'{os.getcwd()}{product.get_image()}')

                file_type = file.filename.split('.')[1]
                file.save(os.path.join(os.getcwd(), f'public/product-img/{product.get_id()}.{file_type}'))
                product.set_image(f'/public/product-img/{product.get_id()}.{file_type}')

            Products.update(id, product)
            return render_template('admin/manage-products/update.html', success=True, product=Products.select(id))

        except:
            return redirect('/admin/products')

    else:
        return render_template('admin/manage-products/update.html', product=Products.select(id))


@router.get('/delete/<id>')
def delete_product(id):
    try:
        product = Products.select(id)
        os.unlink(f'{os.getcwd()}{product.get_image()}')
        Products.delete(id)
        
        return redirect('/admin/products')

    except KeyError:
        return redirect('/admin/products')
