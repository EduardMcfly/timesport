from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Integer, String

from database import db


class Training(db.Model):
    __tablename__ = 'trainings'
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    turns = Column(Integer())
    track_id = Column(Integer, ForeignKey('tracks.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
