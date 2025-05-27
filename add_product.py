from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    prod_name = StringField('Название', validators=[DataRequired()])
    prod_volume = StringField('Объем', validators=[DataRequired()])
    prod_category = StringField('Категория', validators=[DataRequired()])
    price = DecimalField('Цена', validators=[DataRequired()])
    description = TextAreaField('Состав')
    img_prod = StringField('Ссылка на изображение')
    submit = SubmitField('Добавить продукт')
    save = SubmitField('Сохранить изменения')
