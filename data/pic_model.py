import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Picture(SqlAlchemyBase):
    __tablename__ = 'pictures'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    filename = sa.Column(sa.String, nullable=False)
    create_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    owner = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)

    publisher = orm.relationship('User', back_populates='pictures')
