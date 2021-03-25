from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from database import db


class CategoryGender(db.Model):
    __tablename__ = 'category_genders'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, (ForeignKey('categories.id')))
    gender_id = Column(Integer, (ForeignKey('genders.id')))
