from flask.helpers import url_for
from flask_login.utils import login_required
from models import Training, Track, Category
from flask import render_template, request, redirect
from sqlalchemy.sql import text
from flask.blueprints import Blueprint
from database import getSession
from utils import query_to_dict
from flask_login import current_user

trainingBp = Blueprint(
    'training',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/training',
)


@trainingBp.route("/trainings", methods=['GET', 'POST'])
@login_required
def trainings():

    session = getSession()
    connection = session.connection()

    results = connection.execute(
        text('''SELECT
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
	ID LEFT JOIN users ON trainings.user_id = users.ID WHERE trainings.user_id = :user_id;'''),
        ({"user_id": current_user.id})
    )
    trainings = query_to_dict(results)
    trainings = session.query(Training, Track, Category).join(
        Track, Category
    ).filter(Training.user_id == current_user.id).all()
    return render_template('trainings.html', trainings=trainings)


@trainingBp.route("/trainingCreate", methods=['GET', 'POST'])
@login_required
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
        try:
            training = Training()
            training.date = date
            training.category_id = category
            training.turns = turns
            training.track_id = track
            training.user_id = current_user.id
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
@login_required
def delete(id):
    session = getSession()
    training = session.query(Training).filter(
        Training.id == id, Training.user_id == current_user.id
    )
    if(training.first()):
        training.delete()
        session.commit()
        return redirect(url_for('training.trainings'))
    return "No tienes acceso"


@trainingBp.route("/charts")
def charts():
    return render_template('charts.html')

@trainingBp.route("/modules")
def modules():
    return render_template('home.html')
