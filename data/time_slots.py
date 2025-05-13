import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class TimeSlot(SqlAlchemyBase):
    __tablename__ = 'time_slots'

    slot_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    start = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)