from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    comment = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв')
