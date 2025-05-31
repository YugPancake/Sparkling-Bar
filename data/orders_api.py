import flask
from flask import request, jsonify
from . import db_session
from .orders import Order
from .order_items import OrderItem
from .cart_items import CartItem
from .products import Product
from flask_login import current_user, login_required
from sqlalchemy import func
from datetime import datetime

blueprint = flask.Blueprint(
    'orders_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/admin/change_order_status', methods=['POST'])
def change_order_status():
    data = request.get_json()
    order_id = data.get('order_id')
    new_status = data.get('new_status')
    
    if not order_id or not new_status:
        return jsonify(success=False, message="Неверные данные"), 400

    db_sess = db_session.create_session()
    order = db_sess.query(Order).filter(Order.o_id == order_id).first()
    
    if not order:
        return jsonify(success=False, message="Заказ не найден"), 404

    order.o_status = new_status
    db_sess.commit()

    return jsonify(success=True)


@blueprint.route('/api/order', methods=['POST'])
def create_order():

    db_sess = db_session.create_session()
    cart_items = db_sess.query(CartItem).filter(CartItem.user_id == current_user.user_id).all()

    order = Order(
        user_id = current_user.user_id,
        o_sum = 0,
        o_status = "обрабатывается"
    )
    db_sess.add(order)
    db_sess.commit()
    """
    
    item_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item_order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.o_id'), nullable=True)
    item_prod_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)
    item_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    item_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
"""
    total_price = 0
    for i in cart_items:
        product = db_sess.query(Product).where(Product.prod_id == i.product_id).first()
        order_item = OrderItem(
            item_order_id = order.o_id,
            item_prod_id = i.product_id,
            item_user_id = current_user.user_id,
            item_amount = i.ci_amount
        )
        db_sess.add(order_item)
        db_sess.delete(i)
        total_price += product.price * i.ci_amount

    order.o_sum = total_price
    db_sess.commit()

    return jsonify(success=True)

@blueprint.route('/api/order/info', methods=['GET'])
def order_info():
    order_id = request.args.get('order_id', type=int)
    if not order_id:
        return jsonify({'error': 'order_id не передан'}), 400
    
    db_sess = db_session.create_session()

    order = db_sess.query(Order).filter(Order.o_id == order_id).first()
    if not order:
        return jsonify({'error': 'Заказ не найден'}), 404

    items = []
    for item in order.order_items:
        product = item.item_prod
        print(f"Product: {product}, name: {getattr(product, 'prod_name', None)}, price: {getattr(product, 'price', None)}, img: {getattr(product, 'img_prod', None)}")
        if product and product.prod_name and product.price is not None and product.img_prod:
            items.append({
                'product_name': product.prod_name,
                'price': product.price,
                'img_prod': product.img_prod,
            })

    return jsonify({
        'order_id': order.o_id,
        'order_sum': order.o_sum,
        'status': order.o_status,
        'date': order.o_date.isoformat(),
        'items': items
    })

@blueprint.route('/api/order/create_direct', methods=['POST'])
@login_required
def create_direct_order():
    """Создание заказа с одним товаром, минуя корзину"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify(success=False, message="Не указан ID товара"), 400

    db_sess = db_session.create_session()
    try:
        # Проверяем существование товара
        product = db_sess.query(Product).filter(Product.prod_id == product_id).first()
        if not product:
            return jsonify(success=False, message="Товар не найден"), 404
        
        # Создаем новый заказ
        order = Order(
            user_id=current_user.user_id,
            o_sum=float(product.price) * quantity,
            o_status="обрабатывается"
        )
        db_sess.add(order)
        db_sess.flush()  # Получаем o_id
        
        # Добавляем товар в заказ
        order_item = OrderItem(
            item_order_id=order.o_id,
            item_prod_id=product_id,
            item_user_id=current_user.user_id,
            item_amount=quantity
        )
        db_sess.add(order_item)
        
        db_sess.commit()
        
        return jsonify(
            success=True,
            order_id=order.o_id,
            message="Заказ успешно создан"
        )
    except Exception as e:
        db_sess.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_sess.close()