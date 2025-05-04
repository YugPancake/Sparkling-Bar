from flask import Flask, render_template
from datetime import datetime
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():   
    return render_template('index.html', title="Главная страница")
    
if __name__ == '__main__':
    db_session.global_init("db/bar.db")
    app.run()    
 