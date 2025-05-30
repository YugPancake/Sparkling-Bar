import flask
from flask import request, jsonify
from . import db_session
from .orders import Order
from sqlalchemy import func
from .cart_items import CartItem
from flask_login import current_user

blueprint = flask.Blueprint(
    'cart_items_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    amount = data.get('amount')
    
    if not product_id or not amount:
        return jsonify(success=False, message="Неверные данные"), 400

    db_sess = db_session.create_session()
    cart_item = db_sess.query(CartItem).filter(
        CartItem.product_id == product_id,
        CartItem.user_id == current_user.user_id
    ).first()
    
    if not cart_item:
        cart_item = CartItem(
            user_id=current_user.user_id,
            product_id=product_id,
            ci_amount=amount
        )
        db_sess.add(cart_item)
        db_sess.commit()
    else:
        cart_item.ci_amount = amount
        db_sess.commit()

    return jsonify(success=True)