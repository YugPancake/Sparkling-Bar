import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_surname = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(12), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(70), index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.role_id'), nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    role = orm.relationship('Role')

    user_reviews = orm.relationship('UserReview', back_populates="user")
    all_reserv = orm.relationship('Reserv', back_populates="user")
    orders = orm.relationship('Order', back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.user_id) 
