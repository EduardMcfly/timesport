from models import Training, Track, Category, User
from flask import render_template, request
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
        name = request.form.get('name')
        password = request.form.get('password')

        session = getSession()
        connection = session.connection()
        try:
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
    return render_template('trainingsViews.html')
