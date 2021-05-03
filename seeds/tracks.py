from database import getSession
from flask_seeder import Seeder, Faker, generator
from models import Track
# All seeders inherit from Seeder

data = [
    {"name": "La Montaña", "location": "Girardot – Tocaima", "size": 1000},
    {"name": "La Laguna", "location": "Guasca"},
    {"name": "Finca Hacienda San Miguel (El Ospicio)", "location": "La Mesa"},
    {"name": "Minas Montecristo ", "location": "Cucunuba"},
    {"name": "Pista De Veloarena Y Enduro La Bonita",
        "location": "Girardot", "size": 2500},
    {"name": "La mugrosa", "location": "Villeta "},
    {"name": "Territorio Chibcha", "location": "Facatativá"},
    {"name": "ninght", "location": "Giradot", "size": 1500},
    {"name": "El Reto ", "location": "Tocancipá y Gachancipá "},
    {"name": "Lenguazaque", "location": "Lenguazaque "},
]


class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):

        session = getSession()
        count = session.query(Track).count()
        if(count != 0):
            return None
        for item in data:
            track = Track()
            track.name = item.get("name")
            track.location = item.get("name")
            track.size = item.get("size") or 5000
            self.db.session.add(track)
