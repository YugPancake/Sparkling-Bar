import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    o_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    o_sum = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)  # DECIMAL(10,2)
    o_status = sqlalchemy.Column(sqlalchemy.Enum('выполнен', 'готовится', 'обрабатывается'), nullable=False)  # ENUM
    o_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship('User')

    order_items = orm.relationship('OrderItem', back_populates="item_order")
