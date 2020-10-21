from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from database import db


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
