import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class UserReview(SqlAlchemyBase):
    __tablename__ = 'user_reviews'

    review_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    created_comment = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship('User')
    product = orm.relationship('Product')


    def to_dict(self, only=None):
        data = {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "comment": self.comment,
            "created_comment": self.created_comment
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data