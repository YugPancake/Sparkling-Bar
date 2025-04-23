import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class UserReview(SqlAlchemyBase):
    __tablename__ = 'user_reviews'

    review_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    created_comment = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship('User')
    product = orm.relationship('Product')


