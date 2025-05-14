import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Table(SqlAlchemyBase):
    __tablename__ = 'tables'

    table_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    table_number = sqlalchemy.Column(sqlalchemy.String(10), nullable=False)
    table_price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    
    def to_dict(self, only=None):
        data = {
            "table_id": self.table_id,
            "table_number": self.table_number,
            "table_price": self.table_price
        }
        if only:
            return {key: data[key] for key in only if key in data}
        return data