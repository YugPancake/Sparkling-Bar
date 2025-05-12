from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import func
from datetime import datetime
from data import db_session
from data.users import User
from data.roles import Role
from data.products import Product
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.fill_products import fill_products_from_csv
from login import LoginForm
from register import RegisterForm
from add_product import ProductForm
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def delete_users_without_password():
    db_sess = db_session.create_session()
    users_without_password = db_sess.query(User).filter((User .password == None) | (User .password == '')).all()
    
    # Удаляем пользователей без пароля
    for user in users_without_password:
        db_sess.delete(user)
    
    # Сохраняем изменения в базе данных
    db_sess.commit()
    
    return len(users_without_password)  # Возвращаем количество удаленных пользователей

if __name__ == "__main__":
    db_session.global_init("db/bar.db")
    deleted_count = delete_users_without_password()
    print(f"Удалено пользователей без пароля: {deleted_count}")
