import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class OrderItem(SqlAlchemyBase):
    __tablename__ = 'order_items'

    item_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item_order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.o_id'), nullable=True)
    item_prod_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)
    item_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    item_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)

    item_order = orm.relationship('Order')
    item_prod = orm.relationship('Product')
    item_user = orm.relationship('User', back_populates='order_items')
    
    def to_dict(self, only=None):
        data = {
            "item_id": self.item_id,
            "item_order_id": self.item_order_id,
            "item_prod_id": self.item_prod_id,
            "item_user_id": self.item_prod_id,
            "item_amount": self.item_prod_id
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data

