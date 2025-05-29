from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import func
from datetime import datetime
from data import db_session
from data.users import User
from data.roles import Role
from data.products import Product
from data.time_slots import TimeSlot;
from data.tables import Table;
from data.reserv import Reserv;
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.fill_products import fill_products_from_csv
from login import LoginForm
from register import RegisterForm
from add_product import ProductForm
import re
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


def get_time_slots():
    db_sess = db_session.create_session()

    # Данные для временных слотов
    slots_data = [
        ("21:00", "22:00"),
        ("22:00", "23:00"),
        ("23:00", "00:00"),
        ("00:00", "01:00"),
        ("01:00", "02:00"),
        ("02:00", "03:00"),
        ("03:00", "04:00"),
    ]

    for start_str, end_str in slots_data:
        start_time = datetime.datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_str, "%H:%M").time()


        existing_slot = db_sess.query(TimeSlot).filter(
            TimeSlot.start == start_time,
            TimeSlot.end == end_time
        ).first()

        if existing_slot is None:
            slot = TimeSlot(start=start_time, end=end_time)
            db_sess.add(slot)

    db_sess.commit()
    print("Временные слоты успешно добавлены (если их не было).")
    
    time_slots = db_sess.query(TimeSlot).all()
    tables = db_sess.query(Table).all()
    db_sess.close()
    
    for slot in time_slots:
        print(f"Start: {slot.start}, End: {slot.end}")
    for table in tables:
        print(table.table_number)

def fill_tables():
    db_sess = db_session.create_session()
    
    tables = [
        Table(table_number='1', table_price=500.00),
        Table(table_number='2', table_price=500.00),
        Table(table_number='3', table_price=900.00),
        Table(table_number='4', table_price=1200.00),
        Table(table_number='5', table_price=1500.00),
        Table(table_number='6', table_price=2000.00)
    ]
    
    for table in tables:
        existing_table = db_sess.query(Table).filter(
            Table.table_number == table.table_number
        ).first()
        
        if existing_table is None:
            db_sess.add(table)

    db_sess.commit()
    db_sess.close()
    

def seed_data():
    db_sess = db_session.create_session()
    
    # Заполнение временных слотов
    get_time_slots()

    # Заполнение таблиц
    fill_tables()
    
    
if __name__ == "__main__":
    db_session.global_init("db/bar.db")
    seed_data()
