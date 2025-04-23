import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Reserv(SqlAlchemyBase):
    __tablename__ = 'reserv'

    reserv_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    count_people = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    table_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tables.table_id'), nullable=False)
    reserv_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    time_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('time_slots.slot_id'), nullable=False)
    status_r = sqlalchemy.Column(sqlalchemy.Enum('действует', 'отмена', 'прошла'), nullable=False)

    user = orm.relationship('User')
    table = orm.relationship('Table')
    time = orm.relationship('TimeSlot')


