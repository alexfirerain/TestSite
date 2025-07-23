import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from .pic_model import Picture
from .consideration_model import Consideration


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    create_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    level = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    considerations = orm.relationship("Consideration",
                                      order_by=Consideration.id, back_populates='publisher')
    pictures = orm.relationship("Picture",
                                order_by=Picture.id, back_populates='publisher')

    def set_username(self, newname):
        self.name = newname

    def __repr__(self):
        return f'<User: {self.name}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
