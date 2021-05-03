from datetime import datetime
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Integer, Time

from database import db


class Training(db.Model):
    __tablename__ = 'trainings'
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    turns = Column(Integer())
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def getDuration(self):
        a: datetime = self.start_time
        b: datetime = self.end_time
        if(a and b):
                return (int(b.hour*60)+b.minute)-(int(a.hour*60)+a.minute)
        return 0
