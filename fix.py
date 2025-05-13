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
from datetime import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


def get_time_slots():
    db_sess = db_session.create_session()
    time_slots = db_sess.query(TimeSlot).all()
    db_sess.close()
    
    # Выводим временные слоты
    for slot in time_slots:
        print(f"Start: {slot.start}, End: {slot.end}")

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
    

if __name__ == "__main__":
    db_session.global_init("db/bar.db")
    fill_tables()
