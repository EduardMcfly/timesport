from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from database import db


class CategoryAge(db.Model):
    __tablename__ = 'category_ages'
    id = Column(Integer, primary_key=True)
    since = Column(Integer)
    until = Column(Integer)
    category_id = Column(Integer, (ForeignKey('categories.id')))
