import os
from datetime import datetime

from flask import Blueprint, jsonify, render_template, url_for, request, redirect
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
def competences():
    session = getSession()
    connection = session.connection()
    results = connection.execute('''SELECT   competences.id, date, category.category AS category,
    Tracks.name AS name_track, Tracks.measure AS masure_track,
    duration_minutes, amount_turned, classification
	FROM public.competences INNER JOIN Tracks ON competences.tracks_id = Tracks.Id
	 INNER JOIN category ON competences.category_id = category.Id;''')
    competences = query_to_dict(results)
    print(competences)
    return render_template('competences.html', competences=competences)


@competenceBp.route("/createCompetences", methods=['GET', 'POST'])
def createCompetences():
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
                "INSERT INTO competences(date, duration_minutes, amount_turned, classification, tracks_id, category_id, registration_id) VALUES( %s, %s, %s, %s, %s, %s, %s)",
                date, duration_minutes, amount_turned, classification, tracks, category_id, name
            )
            # This is to save the data used in the transactions (INSERT, UPDATE, DELETE).
            session.commit()
            return redirect('competences')
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createCompetences.html')
