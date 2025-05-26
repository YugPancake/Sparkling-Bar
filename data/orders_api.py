import flask
from flask import request, jsonify
from . import db_session
from .orders import Order
from sqlalchemy import func

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