from math import prod
from flask import Blueprint, render_template, request, jsonify, session
from data.products import *
from data.order import *

router = Blueprint('viewProducts', __name__, template_folder='./templates')


def filterProducts(filter):
    products = []

    if filter == 'Shoe' or filter == 'Slide':
        for i in Products.list():
            if (i.get_category().endswith(filter)):
                products.append(i)

    else:
        for i in Products.list():
            if (i.get_brand() == filter):
                products.append(i)

    return products


def sortProducts(sortBy, list):
    if sortBy == 'A to Z':
        return sorted(list, key=lambda product: product.get_name())

    elif sortBy == 'price low to high':
        return sorted(list, key=lambda product: int(product.get_price()))

    elif sortBy == 'price high to low':
        return sorted(list, key=lambda product: int(product.get_price()), reverse=True)

    elif sortBy == 'newest':
        return reversed(list)


@router.get('/products/retrive')
def getAllProducts():
    products = []
    query = request.args.get('category')
    sort = request.args.get('sort')

    productList = sortProducts(sort, Products.list()) if sort else Products.list()

    for i in productList:
        productDetails = {
            'id': i.get_id(),
            'name': i.get_name(),
            'image': i.get_image(),
            'brand': i.get_brand(),
            'description': i.get_description(),
            'category': i.get_category(),
            'price': i.get_price(),
            'stock': i.get_stock()
        }

        if i.get_stock() != 0:
            if query:
                if productDetails.get('category').startswith(query):
                    products.append(productDetails)

            else:
                products.append(productDetails)

    return jsonify(products)


@router.get('/men')
def men_products():
    return render_template('customer/products/product.html', category='Men')


@router.get('/women')
def women_products():
    return render_template('customer/products/product.html', category='Women')


@router.get('/accessories')
def accessories():
    return render_template('customer/products/product.html', category='Accessories')


@router.get('/product/<id>')
def men_product_info(id):
    product_list = []

    for i in Products.list():
        if i.get_category().startswith('Men'):
            product_list.append(i)

        elif i.get_category().startswith('Women'):
            product_list.append(i)

        else:
            product_list.append(i)

    products = {}
    for x in Products.list():
        p = Products.select(x.get_id())
        products[p.get_id()] = p.totalQtySold

    recommand_products = []
    e = sorted(products.items(), key=lambda x: x[1], reverse=True)

    for item in e[:4]:
        recommand_products.append(Products.select(item[0]))

    return render_template('customer/products/product-info.html', product=Products.select(id), recommanded_products=recommand_products)