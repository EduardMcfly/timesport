from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Time

from database import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    duration_min = Column(Integer)
    duration_max = Column(Integer)
    categoryAges = relationship("CategoryAge")
    trainings = relationship("Training")
    