from data.user import *
import routes.customer.main as customerRoutes
import routes.admin.main as adminRoutes
import routes.admin.auth as adminAuth
from data.products import *
import flask
import os

app = flask.Flask(__name__, template_folder='./templates', static_folder='./public')
app.register_blueprint(customerRoutes.router)
app.register_blueprint(adminRoutes.router)
app.register_blueprint(adminAuth.router)

app.secret_key = 'myvEryS3crEtk3y'


@app.before_request
def check_user():
    try:
        Users.select(flask.session['userid'])
        Users.get_cart(flask.session['userid'])
        return None
        
    except KeyError:
        try:
            flask.session.pop('userid')
            
        except KeyError:
            pass


@app.route('/')
def home_page():
    products = []

    for i in Products.list():
        products.append(i)

    return flask.render_template('customer/home.html', products=products[:4])


@app.route('/upload/<id>')
def image_file(id):
    return flask.send_from_directory(os.getcwd(), f'public/product-img/{id}')


@app.errorhandler(404)
def page_not_found(error):
    msg = "We've searched high and low but we couldn't find what you are looking for :("
    return flask.render_template('error.html', error_type='404 Not Found', error_msg=msg)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
