from flask import Blueprint
from routes.customer.auth import router as customerAuth
from routes.customer.products import router as viewProducts
from routes.customer.cart import router as cart
from routes.customer.payment import router as payment
from routes.customer.profile import router as profile
from routes.customer.support import router as support

router = Blueprint('customer', __name__)

router.register_blueprint(customerAuth)
router.register_blueprint(viewProducts)
router.register_blueprint(cart)
router.register_blueprint(payment)
router.register_blueprint(profile)
router.register_blueprint(support)
