import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class CartItem(SqlAlchemyBase):
    __tablename__ = 'cart_items'

    ci_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)
    ci_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    user = orm.relationship('User')
    product = orm.relationship('Product')
    
    def to_dict(self, only=None):
        data = {
            "ci_id": self.ci_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "ci_amount": self.ci_amount,
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data