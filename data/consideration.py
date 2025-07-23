import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Consideration(SqlAlchemyBase):
    """
    Cоображение (мысль/заметка) пользователя.

    Attributes:
        id (int): Уникальный идентификатор соображения.
        title (str): Заголовок соображения.
        content (str): Содержание соображения.
        create_date (datetime): Момент публикации соображения.
        is_private (bool): Частное соображение (по умолчанию нет).
        origin (int): Идентификатор соображающего пользователя.
        publisher (User): Связь с моделью User.
    """
    __tablename__ = 'considerations'

    id = sa.Column(sa.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sa.Column(sa.String,
                              nullable=True)
    content = sa.Column(sa.String,
                                nullable=True)
    create_date = sa.Column(sa.DateTime,
                                    default=datetime.datetime.now())
    is_private = sa.Column(sa.Boolean,
                                   default=False)
    origin = sa.Column(sa.Integer,
                       sa.ForeignKey("users.id"))
    publisher = orm.relationship('User')

    def __str__(self):
        return f'<Соображение: {self.origin}@{self.create_date}>'

    def __repr__(self):
        return f'<Соображение: {self.title}: {self.content}>'
