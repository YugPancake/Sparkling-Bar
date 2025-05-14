from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data import db_session, reserv_api
from data.users import User
from data.roles import Role
from data.products import Product
from data.tables import Table;
from data.time_slots import TimeSlot;
from data.reserv import Reserv;
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.fill_products import fill_products_from_csv
from login import LoginForm
from register import RegisterForm
from add_product import ProductForm
import re
from requests import get, post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    
    return db_sess.query(User).filter(User.user_id == user_id).first()

@app.route('/', methods=['GET', 'POST'])
def home():
    db_sess = db_session.create_session()
    
    products = db_sess.query(Product).order_by(func.random()).limit(8).all()  
    products_list = [product.to_dict() for product in products]
    
    return render_template('index.html', title="Главная страница", products=products_list, current_user=current_user)

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db_sess = db_session.create_session()
    
    products = db_sess.query(Product).order_by(func.random()).all()  
    products_list = [product.to_dict() for product in products]
    return render_template('catalog.html', title="Каталог", products=products_list, current_user=current_user)

@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
    db_sess = db_session.create_session()
    
    products_for_try_also = db_sess.query(Product).order_by(func.random()).limit(8).all()  
    products_try_also_list = [product.to_dict() for product in products_for_try_also]
    
    product = db_sess.query(Product).get(id)
    product_name = product.prod_name
    
    pattern = r',\s*(?![^()]*\))'
    items = re.split(pattern, product.description)
    description_list = [item.strip().capitalize() for item in items]

    return render_template('product.html', title=product_name, product=product, products=products_try_also_list, description_list=description_list,   current_user=current_user)

@app.route('/table_map')
def table_map():
    db_sess = db_session.create_session()
    
    tables = db_sess.query(Table).all()
    tables_list = [table.to_dict() for table in tables]
    
    time_slots = db_sess.query(TimeSlot).all()
    time_slots_list = [time.to_dict() for time in time_slots]
    
    return render_template('table_map.html', title="Карта столов", tables=tables_list, time_slots=time_slots_list, current_user=current_user)

@app.route('/profile')
def profile():
    return render_template('profile.html', title="Ваш профиль")

@app.route('/admin')
def admin():
    return render_template('admin.html', title="Админ")

@app.route('/cart')
def cart():
    return render_template('cart.html', title="Корзина")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        else:
            flash('Неправильный email или пароль', 'danger')
       
    return render_template('login.html', form=form, title="Вход")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Пользователь с таким email уже существует", title="Регистрация")
        user = User(
            user_surname=form.surname.data,
            user_name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            role_id=2,
            created_at=datetime.now(),
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    

    return render_template('register.html', form=form, title="Регистрация")

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    db_sess = db_session.create_session()
    if db_sess.query(Product).filter(Product.prod_name == form.prod_name.data).first():
            return render_template('add_product.html',
                                   form=form,
                                   message="Такой продукт уже есть в меню")
    if form.validate_on_submit():
        new_product = Product(
            prod_name=form.prod_name.data,
            prod_volume=form.prod_volume.data,
            prod_category=form.prod_category.data,
            price=form.price.data,
            description=form.description.data,
            img_prod=form.img_prod.data
        )
        db_sess.add(new_product)
        db_sess.commit()
        flash('Продукт успешно добавлен!', 'success')
        return redirect(url_for('add_product'), title="Добавление в меню")

    return render_template('add_product.html', form=form)

@app.route('/get_products')
def get_products():
    category = request.args.get('category')
    
    db_sess = db_session.create_session()

    if category:
        products = db_sess.query(Product).filter(Product.prod_category == category).order_by(func.random()).limit(8).all()
    else:
        products = db_sess.query(Product).order_by(func.random()).limit(8).all()

    products_list = [product.to_dict() for product in products]
    return jsonify({'products': products_list})

if __name__ == '__main__':
    db_session.global_init("db/bar.db")
    app.register_blueprint(reserv_api.blueprint)
    app.run()    
    response_reserv = post('http://127.0.0.1:5000/api/reserv')
    print(response_reserv.json())
 