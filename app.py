import os
from datetime import datetime

from flask import Flask, render_template, url_for

from blueprints import trainingBp, authenticationBp, trackBp
from database import db, getSession, migrate
from models import *
from utils import ext, query_to_dict
from blueprints.competence import competenceBp
from login_manager import login_manager
from blueprints.competence import competenceBp
from blueprints.homePage import homePageBp


static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)

app.register_blueprint(competenceBp)

for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    # pylint: disable=no-member
    app.jinja_env.add_extension(extension)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)
migrate.init_app(app)
login_manager.init_app(app)

app.register_blueprint(trainingBp)
app.register_blueprint(authenticationBp)
app.register_blueprint(trackBp)
app.register_blueprint(homePageBp)


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





@app.route("/login/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/users")
def users():
    session = getSession()
    connection = session.connection()
    results = connection.execute(
        'SELECT id as id_user, name as name_user, password, created_at FROM users'
    )
    users = query_to_dict(results)
    return render_template('users.html', users=users)
