from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship

from database import db


class UserCompetence(db.Model):
    __tablename__ = 'user_competences'
    id = Column(Integer, primary_key=True)
    duration = Column(Integer())
    turns = Column(Integer())
    user_id = Column(Integer, ForeignKey('users.id'))
    competences_id = Column(Integer, ForeignKey('competences.id'))