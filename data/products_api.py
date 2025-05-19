import flask
from flask import request, jsonify
from . import db_session
from .products import Product
from sqlalchemy import func

blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    
    db_sess = db_session.create_session()

    if category:
        products = db_sess.query(Product).filter(Product.prod_category == category).order_by(func.random()).limit(8).all()
    else:
        products = db_sess.query(Product).order_by(func.random()).limit(8).all()

    products_list = [product.to_dict() for product in products]
    return jsonify({'products': products_list})