from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date
from sqlalchemy.orm import relationship

from database import db

class Competence(db.Model):
    __tablename__ = 'competences'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    track_id= Column(Integer,ForeignKey('tracks.id'))
    category_id = Column(Integer,(ForeignKey('categories.id')))
    user_id = Column(Integer,ForeignKey('users.id'))
    userCompetences = relationship("UserCompetence")