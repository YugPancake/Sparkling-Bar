import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class TimeSlot(SqlAlchemyBase):
    __tablename__ = 'time_slots'

    slot_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    start = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    table_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tables.table_id'), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Enum('доступен', 'недоступен'), nullable=False)

    table = orm.relationship('Table')
    
    all_reserv = orm.relationship('Reserv', back_populates="time")
    

