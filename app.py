import os
from sqlalchemy import or_
from datetime import datetime
from typing import Union
from flask import Flask, render_template, url_for
from flask_login import current_user
from flask_login.utils import login_required
from flask_seeder import FlaskSeeder
from blueprints import trainingBp, authenticationBp, trackBp
from database import db, getSession, migrate
from models import *
from utils import ext
from utils import ext, getPerformance, getPerformanceCompetence
from utils.charts import dataChartTrainings, dataChartCompetences
from blueprints.competence import competenceBp
from login_manager import login_manager
from blueprints.homePage import homePageBp
from sqlalchemy import func, or_


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


@app.template_filter('color')
def color(value):
    if value > 80:
        return '#ff8800'
    if value > 60:
        return '#ef9835'
    if value > 40:
        return '#e4ff00'
    if value > 20:
        return '#e4f746'
    if value > 10:
        return '#fb2300e5'
    return '#f15e47e5 '


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
    labelsCompetences, dataCompetences = dataChartCompetences()
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
            "labels": labelsCompetences,
            "data": dataCompetences,
            "name": "Rendimiento Competencias",
            "dataset": {
                "label": "Rendimiento ",
                "color": "rgb(141 30 2 / 32%)"
            }
        },
    ]

    def getTrending(key: str, model: Union[Track, Category], limit=8):
        session = getSession()
        sumColumn = (
            func.count(getattr(Training, key)) +
            func.count(getattr(Competence, key))
        ).label("count")
        query = session.query(
            sumColumn,
            model
        ).join(Training, Competence, UserCompetence, isouter=True)\
            .filter(or_(Training.user_id == current_user.id, UserCompetence.user_id == current_user.id))\
            .group_by(model.id).order_by(sumColumn.desc())\
            .limit(limit)
        return query.all()

    popularTracks = getTrending('track_id', Track)
    trendingCategories = getTrending('category_id', Category)

    totalCategories = sum(list(map(lambda x: x.count, trendingCategories)))

    return render_template(
        'main.html',
        charts=charts,
        popularTracks=popularTracks,
        trendingCategories=trendingCategories,
        totalCategories=totalCategories,
    )


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
