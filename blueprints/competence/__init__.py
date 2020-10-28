from flask import Blueprint, render_template, request, redirect
from sqlalchemy.sql import text

from database import db, getSession, migrate
from models import *
from utils import query_to_dict


competenceBp = Blueprint(
    'competence',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/cometence'
)


@competenceBp.route("/competences")
def index():
    session = getSession()
    connection = session.connection()
    results = connection.execute('''SELECT   competences.id, date, categories.name AS category,
    tracks.name AS name, tracks.size AS masure_track,
    duration_minutes, amount_turned, classification
	FROM public.competences INNER JOIN tracks ON competences.track_id = tracks.id
	 INNER JOIN categories ON competences.category_id = categories.id;''')
    competences = query_to_dict(results)
    print(competences)
    return render_template('competences.html', competences=competences)


@competenceBp.route("/createCompetences", methods=['GET', 'POST'])
def create():
    method = request.method
    if(method == 'POST'):
        date = request.form.get('date')
        category_id = request.form.get('Category')
        tracks = request.form.get('track')
        duration_minutes = request.form.get('duration_minutes')
        amount_turned = request.form.get('amount_turned')
        classification = request.form.get('classification')
        name = request.form.get('name')
        session = getSession()
        print(session)
        connection = session.connection()
        try:
            connection.execute(
                "INSERT INTO competences(date, duration_minutes, amount_turned, classification, track_id, category_id, user_id) VALUES( %s, %s, %s, %s, %s, %s, %s)",
                date, duration_minutes, amount_turned, classification, tracks, category_id, name
            )
            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return redirect('competences')
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createCompetences.html')
