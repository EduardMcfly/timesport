from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Date

from database import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    duration = Column(Integer)
    categoryAges = relationship("CategoryAge")
