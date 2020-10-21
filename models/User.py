from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String

from database import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128))
    lastname = Column(String(128))
    password = Column(String(128), nullable=False)
    tracks = relationship("Track")
