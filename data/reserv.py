import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Reserv(SqlAlchemyBase):
    __tablename__ = 'reserv'

    reserv_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.user_id'), nullable=False)
    table_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tables.table_id'), nullable=False)
    slot_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('time_slots.slot_id'), nullable=False)
    reserv_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)

    user = orm.relationship('User', back_populates='reservations')
    table = orm.relationship('Table', back_populates='all_reserv')
    slot = orm.relationship('TimeSlot', back_populates='all_reserv')
    
    def to_dict(self, only=None):
        data = {
            "reserv_id": self.reserv_id,
            "user_id": self.user_id,
            "table_id": self.table_id,
            "reserv_date": self.reserv_date,
            "price": self.price
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data

