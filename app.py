from flask import Flask, render_template
from datetime import datetime
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()

@app.route('/', methods=['GET', 'POST'])
def home():   
    return render_template('index.html', title="Главная страница")

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/table_map')
def table_map():
    return render_template('table_map.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
    
if __name__ == '__main__':
    db_session.global_init("db/bar.db")
    app.run()    
 