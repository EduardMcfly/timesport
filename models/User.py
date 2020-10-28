from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String
from flask_login.mixins import UserMixin

from database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    tracks = relationship("Track")
