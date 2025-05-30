import flask
from flask import request, jsonify
from . import db_session
from .orders import Order
from sqlalchemy import func
from .cart_items import CartItem
from .products import Product
from flask_login import current_user
from sqlalchemy import func

blueprint = flask.Blueprint(
    'cart_items_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/cart/get_id/<int:prod_id>', methods=['GET'])
def get_cart_item_id(prod_id):
    db_sess = db_session.create_session()
    try:
        cart_item = db_sess.query(CartItem).filter(
            CartItem.product_id == prod_id,
            CartItem.user_id == current_user.user_id
        ).first()
        
        if not cart_item:
            return jsonify(success=False, message="Товар не найден в корзине"), 404
        
        return jsonify(success=True, ci_id=cart_item.ci_id)
    except sqlalchemy.exc.SQLAlchemyError as e:
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()

@blueprint.route('/api/cart/increase/<int:ci_id>', methods=['POST'])
def increase_cart_item(ci_id):
    db_sess = db_session.create_session()
    try:
        cart_item = db_sess.query(CartItem).filter(
            CartItem.ci_id == ci_id,
            CartItem.user_id == current_user.user_id
        ).first()
        
        if not cart_item:
            return jsonify(success=False, message="Товар не найден в корзине"), 404
        
        cart_item.ci_amount += 1
        db_sess.commit()
        
        return jsonify(success=True, new_amount=cart_item.ci_amount)
    except sqlalchemy.exc.SQLAlchemyError as e:
        db_sess.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()

@blueprint.route('/api/cart/decrease/<int:ci_id>', methods=['POST'])
def decrease_cart_item(ci_id):
    db_sess = db_session.create_session()
    try:
        cart_item = db_sess.query(CartItem).filter(
            CartItem.ci_id == ci_id,
            CartItem.user_id == current_user.user_id
        ).first()
        
        if not cart_item:
            return jsonify(success=False, message="Товар не найден в корзине"), 404
        
        if cart_item.ci_amount > 1:
            cart_item.ci_amount -= 1
            db_sess.commit()
            return jsonify(success=True, new_amount=cart_item.ci_amount)
        else:
            db_sess.delete(cart_item)
            db_sess.commit()
            return jsonify(success=True, new_amount=0)
    except sqlalchemy.exc.SQLAlchemyError as e:
        db_sess.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()

@blueprint.route('/api/cart/remove/<int:ci_id>', methods=['DELETE'])
def remove_cart_item(ci_id):
    db_sess = db_session.create_session()
    try:
        cart_item = db_sess.query(CartItem).filter(
            CartItem.ci_id == ci_id,
            CartItem.user_id == current_user.user_id
        ).first()
        
        if not cart_item:
            return jsonify(success=False, message="Товар не найден в корзине"), 404
        
        db_sess.delete(cart_item)
        db_sess.commit()
        
        return jsonify(success=True)
    except sqlalchemy.exc.SQLAlchemyError as e:
        db_sess.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()

@blueprint.route('/api/cart/total', methods=['GET'])
def get_cart_total():
    db_sess = db_session.create_session()
    try:
        total_info = db_sess.query(
            func.sum(CartItem.ci_amount * Product.price),
            func.sum(CartItem.ci_amount)
        ).join(
            Product, CartItem.product_id == Product.prod_id
        ).filter(
            CartItem.user_id == current_user.user_id
        ).first()
        
        total_price = total_info[0] or 0
        total_items = total_info[1] or 0
        
        return jsonify(
            success=True,
            total_price=float(total_price),
            total_items=total_items
        )
    except sqlalchemy.exc.SQLAlchemyError as e:
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()

@blueprint.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    amount = data.get('amount')
    
    if not product_id or not amount:
        return jsonify(success=False, message="Неверные данные"), 400

    db_sess = db_session.create_session()
    try:
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
        else:
            cart_item.ci_amount = amount
        
        db_sess.commit()
        return jsonify(success=True)
    except sqlalchemy.exc.SQLAlchemyError as e:
        db_sess.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()