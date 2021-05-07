from blueprints.training import trainingsAll
import os
from datetime import datetime
from typing import List
from flask import Flask, render_template, url_for
from flask_login import current_user
from flask_login.utils import login_required
from flask_seeder import FlaskSeeder
from blueprints import trainingBp, authenticationBp, trackBp
from database import db, getSession, migrate
from models import *
from utils import ext, getPerformance, getPerformanceCompetence
from utils.charts import dataChartTrainings
from blueprints.competence import competenceBp
from login_manager import login_manager
from blueprints.homePage import homePageBp


static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)


for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    # pylint: disable=no-member
    app.jinja_env.add_extension(extension)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)
migrate.init_app(app)
login_manager.init_app(app)

seeder = FlaskSeeder()
seeder.init_app(app, db)

app.register_blueprint(homePageBp)
app.register_blueprint(competenceBp)
app.register_blueprint(trainingBp)
app.register_blueprint(authenticationBp)
app.register_blueprint(trackBp)


@app.template_filter('date_format')
def filter_datetime(value: datetime, fmt="%Y:%M:%d"):
    return value.strftime(fmt)


@app.context_processor
def inject_dict_for_all_templates():
    return dict(
        static=lambda path: url_for('static', filename=path),
        url=lambda path: url_for(path)
    )


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@app.route("/main")
@login_required
def main():
    labels, data = dataChartTrainings()

    charts = [
        {
            "id": "trainings_chart",
            "labels": labels,
            "data": data, 
            "name": "Rendimiento Entrenamientos",
            "dataset": {
                "label": "Rendimiento",
                "color": "rgb(241 230 224 / 12%)"
            }
        },
        {
            "id": "competences_chart",
            "labels": labels,
            "data": data,
            "name": "Rendimiento Competencias",
            "dataset": {
                "label": "Rendimiento ",
                "color": "rgb(141 30 2 / 32%)"
            }
        },
    ]
    return render_template('main.html', charts=charts)

@app.route("/user")
def user():
    user = User.query.get(2)
    year = user.getYearsOld()
    print(year)

@competenceBp.route("/graphics")
def charts():
    session = getSession()
    competences = session.query(Competence, Track, UserCompetence, Category).join(Track, UserCompetence, Category).filter(
        UserCompetence.user_id == current_user.id,
    ).limit(8).all()

    labelss = []
    datas = []
    for item in competences:
        performance = getPerformanceCompetence(
            item.Competence, item.Track, item.Category, item.UserCompetence
        )
        datas.append(performance)
        labelss.append(item.Competence.name_competence)
    return render_template('charts.html', labelss=labelss, datas=datas)
