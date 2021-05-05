from flask_seeder import Seeder
from models import Gender
# All seeders inherit from Seeder

data = [
    {"name": "Femenino"},
    {"name": "Masculino"},
]


class GenderSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        count = self.db.session.query(Gender).count()
        if count == 0:
            for item in data:
                gender = Gender()
                gender.name = item.get("name")
                self.db.session.add(gender)
