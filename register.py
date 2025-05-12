from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=12, max=12)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
