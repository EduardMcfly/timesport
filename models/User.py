from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from database import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    password = Column(String(128))
