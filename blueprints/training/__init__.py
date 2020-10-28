from flask.globals import session
from flask.helpers import url_for
from models import Training, Track, Category, User
from flask import render_template, request, redirect
from flask.blueprints import Blueprint
from database import getSession
from utils import query_to_dict

trainingBp = Blueprint(
    'training',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/trainig'
)


@trainingBp.route("/trainings", methods=['GET', 'POST'])
def trainings():

    session = getSession()
    connection = session.connection()
    results = connection.execute('''SELECT
	trainings.ID,
	DATE,
	categories.NAME AS categoria,
	tracks.NAME AS name_track,
	tracks.SIZE AS masure_track,
	users.NAME AS usuario,
	turns 
FROM
	PUBLIC.trainings
	INNER JOIN tracks ON PUBLIC.trainings.track_id = tracks.
	ID INNER JOIN categories ON trainings.category_id = categories.
	ID LEFT JOIN users ON trainings.user_id = users.ID;''')
    #trainings = session.query(Training).join(Track).all()
    trainings = query_to_dict(results)
    return render_template('trainings.html', trainings=trainings)


@trainingBp.route("/trainingCreate", methods=['GET', 'POST'])
def create():
    method = request.method
    if(method == 'POST'):
        print(request.form)
        print(request.form.get('date'))
        date = request.form.get('date')
        category = request.form.get('category')
        turns = request.form.get('turns')
        track = request.form.get('track')
        session = getSession()
        connection = session.connection()
        try:
            training = Training()
            training.date = date
            training.category_id = category
            training.turns = turns
            training.track_id = track
            training.user_id = 2
            session.add(training)

            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return redirect(url_for('training.trainings'))
        except Exception as error:
            session.rollback()
            raise error
    session = getSession()
    categories = session.query(Category).all()
    tracks = session.query(Track).all()
    return render_template('create.html', categories=categories, tracks=tracks)


@trainingBp.route("/trainig/delete/<int:id>")
def delete(id):
    session = getSession()
    training = session.query(Training).filter(Training.id == id)
    training.delete()
    session.commit()
    return redirect(url_for('training.trainings'))


@trainingBp.route("/charts")
def charts():
    return render_template('charts.html')
