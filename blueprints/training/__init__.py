from flask import render_template, request
from flask.blueprints import Blueprint
from database import getSession
from utils import query_to_dict

trainigBp = Blueprint(
    'training',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/trainig'
)


@trainigBp.route("/trainings")
def trainings():

    session = getSession()
    connection = session.connection()
    results = connection.execute('''SELECT trainings.id, date, category.name AS categoria,
    tracks.name AS name_track, tracks.distance AS masure_track, 
	users.name AS usuario,
   turns
	FROM public.trainings  INNER JOIN tracks ON public.trainings.tracks_id = tracks.id
	 INNER JOIN category ON trainings.category_id = category.id
		LEFT JOIN users ON trainings.user_id = users.id;''')
    trainings = query_to_dict(results)
    return render_template('trainings.html', trainings=trainings)


@trainigBp.route("/trainingCreate", methods=['GET', 'POST'])
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
