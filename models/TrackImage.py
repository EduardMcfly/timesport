from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey

from database import db


class TrackImage(db.Model):
    __tablename__ = 'track_images'
    id = Column(Integer, primary_key=True)
    src = Column(String(90))
    track_id = Column(Integer, ForeignKey('tracks.id'))
