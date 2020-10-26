from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Integer, String

from database import db


class Training(db.Model):
    __tablename__ = 'training'
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    turns = Column(Integer())
    track_id = Column(Integer, ForeignKey('track.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
