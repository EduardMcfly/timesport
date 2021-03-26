from datetime import datetime
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date
from flask_login.mixins import UserMixin


from database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    gender_id = Column(Integer, ForeignKey('genders.id'))
    dateBirth = Column(Date)

    def getYearsOld(self):
        born = self.dateBirth
        if (born):
            today = datetime.today()
            return (
                today.year - born.year -
                ((today.month, today.day) < (born.month, born.day))
            )
        else:
            return 18

    tracks = relationship("Track")
    userCompetences = relationship("UserCompetence")
