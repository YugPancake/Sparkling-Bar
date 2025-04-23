import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    prod_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    prod_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    img_prod = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    order_items = orm.relationship('OrderItem', back_populates="item_prod")