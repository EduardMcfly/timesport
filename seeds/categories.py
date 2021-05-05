from flask_seeder import Seeder
from models import Category, CategoryAge
from database import getSession

data = [
    {
        "name": "Profesionales (PRO)", "min": 90, "max": 120, "category_ages": [{
        "since": 15
    }]},
    {
        "name": "Enduro 1 (E1)", "min": 90, "max": 120, "category_ages": [{"since": 13, "until": 23}]
    },
    {
        "name": "Enduro 2 (E2)", "min": 90, "max": 120, 
        "category_ages": [{"since": 24, "until": 37}]
    },
    {
        "name": "Enduro 3 (E3)", "min": 90, "max": 120, 
        "category_ages": [{"since": 24, "until": 37}]
    },
    {
        "name": "Master A", "min": 90, "max": 120,
        "category_ages": [{"since": 24, "until": 37}]
    },
    {
        "name": "Master B", "min": 90, "max": 120,      
        "category_ages": [{"since": 38, "until": 47}]
    },
    {
        "name": "Iniciación", "min": 50, "max": 60,      
        "category_ages": [{"since": 48}]},
    {
        "name": "Femenina", "min": 50, "max": 60,
        "category_ages": [{"since": 13}]},
    {
        "name": "Producción nacional (PROMOCIONAL)","min": 50, "max": 90, 
        "category_ages": [{"since": 15}]
    },
    {
        "name": "Junior", "min": 90, "max": 120,      
        "category_ages": [{"since": 13}]
    },
]


class CategorySeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        for item in data:
            category = self.db.session.query(Category).filter(
                Category.name == item.get('name')).first()
            empty = not category
            if (not empty):
                for category_age in item.get('category_ages'):
                    categoryAge = self.db.session.query(CategoryAge).filter(
                        CategoryAge.category_id == category.id
                    ).first() 
                    emptyCategoryAge = not categoryAge
                    if(emptyCategoryAge):
                        categoryAge = CategoryAge()
                    categoryAge.category_id = category.id
                    categoryAge.since = category_age.get('since')
                    categoryAge.until = category_age.get('until')
                    if(emptyCategoryAge):
                        self.db.session.add(categoryAge)
            if (empty):
                category = Category()
            category.name = item.get('name')
            category.duration_min = item.get('min')
            category.duration_max = item.get('max')
            if (empty):
                self.db.session.add(category)
            if(empty):
                self.db.session.commit()
                for category_age in item.get('category_ages'):
                    categoryAge = CategoryAge()
                    categoryAge.category_id = category.id
                    categoryAge.since = category_age.get('since')
                    categoryAge.until = category_age.get('until')
                    self.db.session.add(categoryAge)
        self.db.session.commit()
