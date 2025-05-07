import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    prod_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    prod_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    prod_volume = sqlalchemy.Column(sqlalchemy.String(7), nullable=False)
    prod_category = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    img_prod = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    order_items = orm.relationship('OrderItem', back_populates="item_prod")
    
    def to_dict(self, only=None):
        data = {
            "prod_id": self.prod_id,
            "prod_name": self.prod_name,
            "prod_volume": self.prod_volume,
            "prod_category": self.prod_category,
            "price": self.price,
            "description": self.description,
            "img_prod": self.img_prod
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data