import flask
from flask import request, jsonify
from . import db_session
from .reserv import Reserv
from datetime import datetime

blueprint = flask.Blueprint(
    'reserv_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/reserv', methods=['GET'])
def get_reserv():
    db_sess = db_session.create_session()
    reservs = db_sess.query(Reserv).all()

    occupied_tables = {}

    for item in reservs:
        reserv_data = item.to_dict(only=('reserv_id', 'user_id', 'table_id', 'slot_id', 'reserv_date', 'price'))
        

        reserv_date = reserv_data['reserv_date'].strftime('%Y-%m-%d')
        
        if reserv_date not in occupied_tables:
            occupied_tables[reserv_date] = []
        
        occupied_tables[reserv_date].append({
            'table_id': reserv_data['table_id'],
            'slot_id': reserv_data['slot_id'],
            'price': reserv_data['price']
        })

    try:
        return flask.jsonify({'occupied_tables': occupied_tables})
    except Exception as e:
        print(f"Ошибка при сериализации: {e}")
        return flask.jsonify({'error': str(e)}), 500

@blueprint.route('/api/reserv', methods=['POST'])
def make_reservation():
    data = request.get_json()
    date_str = data.get('date')
    slots = data.get('slots')
    user_id = data.get('user_id')

    if not date_str or not slots or not user_id:
        return jsonify({"success": False, "message": "Недостаточно данных для бронирования."}), 400

    try:
        reserv_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"success": False, "message": "Неверный формат даты."}), 400

    session = db_session.create_session()

    for slot in slots:
        table_id = slot['tableId']
        time_slot_id = slot['timeSlotId']
        price = slot['price']

        existing_reservation = session.query(Reserv).filter_by(
            table_id=table_id,
            slot_id=time_slot_id,
            reserv_date=reserv_date 
        ).first()

        if existing_reservation:
            session.close()
            return jsonify({"success": False, "message": f"Стол {table_id} уже забронирован на это время."}), 400

        new_reservation = Reserv(
            user_id=user_id,
            table_id=table_id,
            slot_id=time_slot_id,
            reserv_date=reserv_date,
            price=price
        )

        session.add(new_reservation)

    session.commit()
    session.close()

    return jsonify({"success": True, "message": "Бронирование успешно создано!"}), 201