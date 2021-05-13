from aws.s3 import s3, bucket
from database import getSession
from flask_seeder import Seeder
from models import Track, TrackImage
import os
import uuid
from  pathlib import Path
# All seeders inherit from Seeder

data = [
    {"name": "La Montaña", "location": "Girardot – Tocaima", "size": 1000,"images":["1.jpg"]},
    {"name": "La Laguna", "location": "Guasca","images":["2.jpg"]},
    {"name": "Finca Hacienda San Miguel (El Ospicio)", "location": "La Mesa","images":["3.jpg"] },
    {"name": "Minas Montecristo ", "location": "Cucunuba","images":["15.jpg"]},
    {"name": "Pista De Veloarena Y Enduro La Bonita",
        "location": "Girardot", "size": 2500,"images":["15.jpg"]},
    {"name": "La mugrosa", "location": "Villeta ","images":["30.jpg"]},
    {"name": "Territorio Chibcha", "location": "Facatativá","images":["31.jpg"]},
    {"name": "ninght", "location": "Giradot", "size": 1500 ,"images":["76.jpg"]},
    {"name": "El Reto ", "location": "Tocancipá y Gachancipá ","images":["fondo2.jpg"]},
    {"name": "Lenguazaque", "location": "Lenguazaque ","images":["24.jpg"]},
]

actual = Path(__file__).parent

path = os.path.join(actual, "images/")

to =  "tracks/"

class Tracks(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):

        session = getSession()
        for item in data:
            track = self.db.session.query(Track).filter(
                Track.name == item.get("name")
            ).first()
            exist = bool(track)
            if not exist: track = Track()
            track.name = item.get("name")
            track.location = item.get("location")
            track.size = item.get("size") or 5000
            if not exist: self.db.session.add(track)
            self.db.session.commit()
            images = item.get("images")
            if images:
                for image in images:
                    haveImage = self.db.session.query(TrackImage).filter(
                        TrackImage.track_id == track.id
                    ).first()

                    if not haveImage:
                        ext = Path(image).suffix
                        namefile = uuid.uuid4().hex + ext
                        file = open(path + image, 'rb')
                        s3.put_object(Bucket=bucket, Key=to + namefile, Body=file)
                        trackImage = TrackImage()
                        trackImage.src = namefile
                        trackImage.track_id = track.id
                        self.db.session.add(trackImage)

