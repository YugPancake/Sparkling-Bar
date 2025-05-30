from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data import db_session, reserv_api, products_api, orders_api, cart_items_api
from data.users import User
from data.roles import Role
from data.orders import Order
from data.cart_items import CartItem
from data.order_items import OrderItem
from data.products import Product
from data.tables import Table
from data.time_slots import TimeSlot
from data.reserv import Reserv
from data.reviews import UserReview
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.fill_products import fill_products_from_csv
from login import LoginForm
from register import RegisterForm
from add_product import ProductForm
from review import ReviewForm
import re
from requests import get, post
from fuzzywuzzy import process
import random
from random import choice

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
    
    products = db_sess.query(Product).order_by(func.random()).all()  
    products_list = [product.to_dict() for product in products]
    
    return render_template('index.html', title="Главная страница", products=products_list, current_user=current_user)

@app.route('/catalog', methods=['GET'])
def catalog():
    db_sess = db_session.create_session()
    
    category = request.args.get('category')
    query = request.args.get('q', '').strip()
    cleaned_query = re.sub(r'\s+', ' ', query).strip()

    products_query = db_sess.query(Product)

    if category:
        print(category)
        products_query = products_query.filter(Product.prod_category == category)

    products = products_query.all()

    if cleaned_query:
        product_names = [product.prod_name for product in products]
        
        matched_names_with_scores = process.extract(cleaned_query, product_names, limit=10)

        matched_products = []
        for name, score in matched_names_with_scores:
            if score > 70:
                matched_product = next((product for product in products if product.prod_name == name), None)
                if matched_product:
                    matched_products.append((matched_product, score))

        matched_products.sort(key=lambda x: x[1], reverse=True)
        matched_products = [product for product, score in matched_products]
    else:
        matched_products = products

    products_list = [product.to_dict() for product in matched_products]
    return render_template('catalog.html', title="Каталог", products=products_list, category=category)


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
    
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = UserReview(
            user_id=current_user.user_id,
            product_id=id,
            comment=form.comment.data,
            created_comment=datetime.now()
        )
        db_sess.add(new_review)
        db_sess.commit()
        flash('Отзыв успешно добавлен!', 'success')
        return redirect(url_for('product', id=id))
    
    reviews = db_sess.query(UserReview).filter_by(product_id=id).order_by(UserReview.created_comment.desc()).all()
    reviews_list = [review.to_dict() for review in reviews]
    
    return render_template('product.html', title=product_name, product=product, products=products_try_also_list, description_list=description_list, reviews=reviews_list, current_user=current_user, form=form)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role_id == 1:
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
    else:
        return redirect(url_for('home'))

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role_id == 1:
        db_sess = db_session.create_session()
        product = db_sess.query(Product).get(id)
        if not product:
            return "Продукт не найден", 404
        
        form = ProductForm()
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            product.prod_name=form.prod_name.data
            product.prod_volume=form.prod_volume.data
            product.prod_category=form.prod_category.data
            product.price=form.price.data
            product.description=form.description.data
            product.img_prod=form.img_prod.data
            db_sess.commit()
            return redirect(f'/product/{id}')
        
        form.prod_name.data=product.prod_name
        form.prod_volume.data=product.prod_volume
        form.prod_category.data=product.prod_category
        form.price.data=product.price
        form.description.data=product.description
        form.img_prod.data=product.img_prod
        return render_template('edit_product.html', form=form, product=product, current_user=current_user)
    else:
        return redirect(url_for('home'))

@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if current_user.role_id == 1:
        db_sess = db_session.create_session()
        product = db_sess.query(Product).get(id)
        if not product:
            return "Продукт не найден", 404
        
        db_sess.delete(product)
        db_sess.commit()
        return redirect('/catalog')
    else:
        return redirect(url_for('home'))

@app.route('/table_map')
def table_map():
    db_sess = db_session.create_session()
    
    tables = db_sess.query(Table).all()
    tables_list = [table.to_dict() for table in tables]
    
    time_slots = db_sess.query(TimeSlot).all()
    time_slots_list = [time.to_dict() for time in time_slots]
    
    return render_template('table_map.html', title="Карта столов", tables=tables_list, time_slots=time_slots_list, current_user=current_user)

@app.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    
    user = db_sess.query(User).filter(User.user_id == current_user.user_id).first()
    orders = db_sess.query(Order).filter(Order.user_id == current_user.user_id).all()
    
    table_orders =[]
    orders_data = []
    for order in orders:
        if order.o_status == "выполнен":
            products = [item.item_prod for item in order.order_items]  
            if not products:
                continue  
            random_product = choice(products) 
            o_sum = f"{order.o_sum}р."
            product_info = "; ".join(f"{prod.prod_name}" for prod in products) 
            orders_data.append({
                'order': order,
                'product_info': product_info,
                'random_product': random_product,
                'o_sum': o_sum
            })
        else:
            reserv = db_sess.query(Reserv).filter(
                Reserv.user_id == current_user.user_id,
                Reserv.reserv_date == order.o_date.date()
            ).first()
            products = [item.item_prod for item in order.order_items]
            product_info = "; ".join(f"{prod.prod_name}" for prod in products)  
            table_number = f"Стол №{reserv.table_id}" if reserv else "Бар"
            table_orders.append({
                'order': order,
                'table': table_number,
                'product_info': product_info
            })

    return render_template('profile.html', user=user, orders=orders, table_orders=table_orders, orders_data=orders_data)


@app.route('/admin')
@login_required
def admin():
    if current_user.role_id == 1:
        db_sess = db_session.create_session()
        orders_in_progress = db_sess.query(Order).filter(Order.o_status != "выполнен").all()
        pending_users = db_sess.query(User).filter(User.is_verified == False).all()
        table_orders =[]
        for order in orders_in_progress:
            reserv = db_sess.query(Reserv).filter(
                Reserv.user_id == current_user.user_id,
                Reserv.reserv_date == order.o_date.date()
            ).first()
            products = [item.item_prod for item in order.order_items]
            product_info = "; ".join(f"{prod.prod_name}" for prod in products) 
            table_number = f"Стол №{reserv.table_id}" if reserv else "Бар"
            table_orders.append({
                'order': order,
                'table': table_number,
                'product_info': product_info
            })

        return render_template('admin.html', title="Админ", table_orders = table_orders, orders_in_progress=orders_in_progress, pending_users=pending_users)
    else:
        return redirect(url_for('home'))
    
@app.route('/confirm_user', methods=['GET', 'POST'])
@login_required
def confirm_user():
    if current_user.role_id != 1:
        return redirect(url_for('home'))

    user_id = request.form.get('user_id')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        flash("Пользователь не найден")
        return redirect(url_for('admin'))

    user.is_verified = True
    db_sess.commit()
    flash(f"Пользователь {user.user_name} подтверждён")
    return redirect(url_for('admin'))

@app.route('/cart')
@login_required
def cart():
    cart_items = []
    total_price = 0
    db_sess = db_session.create_session()
    ci_objects = db_sess.query(CartItem).filter(CartItem.user_id == current_user.user_id).all()
    for i in ci_objects:
        product = db_sess.query(Product).filter(Product.prod_id == i.product_id).first()
        cart_items.append({
            "prod_id": i.product_id,
            "image": product.img_prod,
            "price": product.price,
            "amount": i.ci_amount,
            "title": product.prod_name
        })
        total_price += i.ci_amount * product.price
    print(cart_items)
    return render_template('cart.html', title="Корзина", cart_items=cart_items, total_price=total_price)

@app.route('/order')
@login_required
def order():
    cart_items = []
    total_price = 0
    db_sess = db_session.create_session()
    ci_objects = db_sess.query(CartItem).filter(CartItem.user_id == current_user.user_id).all()
    for i in ci_objects:
        product = db_sess.query(Product).filter(Product.prod_id == i.product_id).first()
        cart_items.append({
            "prod_id": i.product_id,
            "image": product.img_prod,
            "price": product.price,
            "amount": i.ci_amount,
            "title": product.prod_name
        })
        total_price += i.ci_amount * product.price
    print(cart_items)
    return render_template('order.html', title="Ваш заказ", order_items=cart_items, total_price=total_price)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.role_id == 1:  
                return redirect(url_for('admin'))
            else:  
                return redirect(url_for('home'))
        else:
            flash('Неправильный email или пароль', 'danger')
       
    return render_template('login.html', form=form, title="Вход")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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


if __name__ == '__main__':
    db_session.global_init("db/bar.db")
    app.register_blueprint(reserv_api.blueprint)
    app.register_blueprint(products_api.blueprint)
    app.register_blueprint(orders_api.blueprint)
    app.register_blueprint(cart_items_api.blueprint)
    app.run()
 