from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from database import db

class Competence(db.Model):
    __tablename__ = 'competences'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    duration_minutes= Column(Integer())
    amount_turned = Column(Integer())
    classification = Column(Integer())
    track_id= Column(Integer,ForeignKey('tracks.id'))
    category_id = Column(Integer,(ForeignKey('categories.id')))
    user_id = Column(Integer,ForeignKey('users.id'))