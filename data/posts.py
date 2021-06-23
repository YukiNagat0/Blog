import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    title = sa.Column(sa.String, nullable=False)
    image_name = sa.Column(sa.String, nullable=True)
    text = sa.Column(sa.String, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    date = sa.Column(sa.DateTime, nullable=False)
