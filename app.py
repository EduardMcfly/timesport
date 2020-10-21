import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request, url_for
from sqlalchemy.sql import text

from blueprints import trainigBp
from database import db, getSession, migrate
from models import *
from utils import ext, query_to_dict
from blueprints.competence import competenceBp


static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)

app.register_blueprint(competenceBp)

for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    # pylint: disable=no-member
    app.jinja_env.add_extension(extension)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env
print(os.getenv('DATABASE_URL'))
print(os.getenv('SECRET_KEY'))
db.init_app(app)
migrate.init_app(app)

app.register_blueprint(trainigBp)


@app.template_filter('date_format')
def filter_datetime(value: datetime, fmt="%Y:%M:%d"):
    return value.strftime(fmt)


@app.context_processor
def inject_dict_for_all_templates():
    return dict(
        static=lambda path: url_for('static', filename=path),
        url=lambda path: url_for(path)
    )


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/login/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signUp")
def signUp():
    return render_template('signUp.html')


@app.route("/users")
def users():
    session = getSession()
    connection = session.connection()
    results = connection.execute(
        'SELECT id as id_user, name as name_user, password, created_at FROM users'
    )
    users = query_to_dict(results)
    return render_template('users.html', users=users)


@app.route("/tracks")
def tracks():

    session = getSession()
    connection = session.connection()
    results = connection.execute('SELECT * FROM tracks')
    tracks = query_to_dict(results)
    return render_template('tracks.html', tracks=tracks)


@app.route("/createUser", methods=['GET', 'POST'])
def createUser():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('name')
        password = request.form.get('password')

        session = getSession()
        connection = session.connection()
        try:
            # Read this please https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/#Double_asterisks_in_dictionary_literals
            # Options
            # Using alias, example ':nameAlias'
            """ connection.execute(
                "INSERT INTO users(name, password) VALUES(:nameAlias, :password)",
                password=password, nameAlias=name
            ) """

            # Insert with object
            # connection.execute(
            #     text(
            #         """INSERT INTO users(name, password) VALUES(:nameAlias, :password)"""
            #     ),
            #     ({"password": password, "nameAlias": name})
            # )

            # Insert many
            """ connection.execute(
                "INSERT INTO users(name, password) VALUES(%s, %s)",
                (password,  name),
                ("root",  "root")
            ) """
            # The more simple
            # Using multiparams
            connection.execute(
                "INSERT INTO users(name, password) VALUES(%s, %s)",
                name, password
            )

            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createUser.html')


@app.route("/createRegistro", methods=['GET', 'POST'])
def createRegistro():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('Name')
        Username = request.form.get('Username')
        Email = request.form.get('Email')
        password = request.form.get('password')
        passworrd = request.form.get('password')

        session = getSession()
        connection = session.connection()
        try:
            connection.execute(
                "INSERT INTO registration(name, username, email_address, password, confirm_password) VALUES(%s, %s, %s, %s, %s)",
                name, Username, Email, password, passworrd
            )

            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('signUp.html')


@app.route("/createTracks", methods=['GET', 'POST'])
def createTracks():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('name')
        ubiety = request.form.get('ubiety')
        size = request.form.get('size')
        session = getSession()
        connection = session.connection()
        try:
            connection.execute(
                "INSERT INTO tracks(name,ubiety,size) VALUES(%s, %s,%s)",
                name, ubiety, size
            )
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createTracks.html')
