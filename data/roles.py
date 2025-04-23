import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Role(SqlAlchemyBase):
    __tablename__ = 'roles'

    role_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True) 
    role_name = sqlalchemy.Column(sqlalchemy.String(40), nullable=False)  

    users = orm.relationship('User', back_populates="role")
