import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class TimeSlot(SqlAlchemyBase):
    __tablename__ = 'time_slots'

    slot_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    start = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    
    def to_dict(self, only=None):
        data = {
            "slot_id": self.slot_id,
            "start": self.start,
            "end": self.end
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data