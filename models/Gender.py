from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from database import db


class Gender(db.Model):
    __tablename__ = 'genders'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    users = relationship("User")
