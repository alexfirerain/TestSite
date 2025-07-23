import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class File(SqlAlchemyBase):
    __tablename__ = 'users'

