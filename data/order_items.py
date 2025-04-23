import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class OrderItem(SqlAlchemyBase):
    __tablename__ = 'order_items'

    item_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item_order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.o_id'), nullable=False)
    item_prod_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.prod_id'), nullable=False)

    item_order = orm.relationship('Order')
    item_prod = orm.relationship('Product')

    

