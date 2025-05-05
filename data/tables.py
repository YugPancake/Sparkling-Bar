import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Table(SqlAlchemyBase):
    __tablename__ = 'tables'

    table_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    table_number = sqlalchemy.Column(sqlalchemy.String(10), nullable=False)
    table_price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    img_table = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    seating_capacity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    all_reserv = orm.relationship('Reserv', back_populates="table")