from flask import Blueprint, render_template, request, redirect, jsonify
from sqlalchemy.sql import text
from flask.helpers import url_for
from database import db, getSession, migrate
from models import Category, Track, Competence, UserCompetence
from utils import query_to_dict
from flask_login import current_user
from flask_login.utils import login_required


competenceBp = Blueprint(
    'competence',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/competence/static'
)


@competenceBp.route("/competences")
@login_required
def index():
    session = getSession()
    connection = session.connection()

    results = connection.execute(
        text('''
    SELECT
        competences.id,
        competences.date,
        tracks.name as track,
        categories.NAME AS category,
        tracks.size AS track_size
    FROM
        public.competences
        INNER JOIN user_competences ON public.competences.id = public.user_competences.competences_id
        INNER JOIN categories ON competences.category_id = categories.id 
        INNER JOIN tracks ON competences.track_id = tracks.id 
    WHERE
	user_competences.user_id = :user_id;'''),
        ({"user_id": current_user.id})
    )
    competences = query_to_dict(results)
    print(competences)
    competences = session.query(Competence, Track, Category, UserCompetence).join(
        UserCompetence, Track, Category
    ).filter(UserCompetence.user_id == current_user.id).all()
    print(competences)
    return render_template('newcompetences.html', competences=competences)


@competenceBp.route("/competence/<int:id>")
@login_required
def one(id):
    session = getSession()
    competence = session.query(Competence, Track, Category, UserCompetence).join(
        UserCompetence, Track, Category
    ).filter(Competence.id == id, UserCompetence.user_id == current_user.id).first()
    return render_template('competence.html', competence=competence)


@competenceBp.route("/createCompetences", methods=['GET', 'POST'])
@login_required
def create():
    method = request.method
    session = getSession()
    if(method == 'POST'):
        date = request.form.get('date')
        name = request.form.get('name')
        category_id = request.form.get('category')
        track = request.form.get('track')

        competence = Competence()
        competence.date = date
        competence.name_competence = name
        competence.category_id = category_id
        competence.track_id = track
        try:
            session.add(competence)
            session.commit()

            userCompetence = UserCompetence()
            userCompetence.user_id = current_user.id
            userCompetence.competences_id=competence.id
            session.add(userCompetence)
            session.commit()
            return redirect(url_for('competence.index'))
        except Exception as error:
            session.rollback()
            raise error
    categories = session.query(Category).all()
    tracks = session.query(Track).all()
    return render_template('createCompetences.html', categories=categories, tracks=tracks)


@competenceBp.route("/createResults/<int:id>", methods=['GET', 'POST'])
@login_required
def createResults(id):
    method = request.method
    session = getSession()
    userCompetence = session.query(UserCompetence).filter(
        UserCompetence.id == id,
        UserCompetence.user_id == current_user.id
    ).first()
    if(userCompetence.duration and userCompetence.turns):
        return "Ya existe el registro"
    if(method == 'POST'):
        duration = request.form.get('duration')
        turns = request.form.get('turns')
        try:
            userCompetence.user_id = current_user.id
            userCompetence.duration = duration
            userCompetence.turns = turns
            session.add(userCompetence)
            session.commit()
            return redirect(url_for('competence.one', id=userCompetence.competences_id))
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createResults.html', id=id)


@competenceBp.route("/competences/delete/<int:id>")
@login_required
def delete(id):
    session = getSession()
    competence = session.query(Competence).filter(
        Competence.id == id, Competence.user_id == current_user.id
    )
    if(competence.first()):
        competence.delete()
        session.commit()
        return redirect(url_for('competence.index'))
    return "No tienes acceso"


@competenceBp.route("/graphics/<int:id>")
def charts(id):
    session = getSession()
    competence = session.query(Competence).filter(Competence.id == id).first()
    competences = session.query(Competence, UserCompetence).join(UserCompetence).filter(
        Competence.date <= competence.date,
        UserCompetence.user_id == current_user.id,
        Competence.track_id == competence.track_id
    ).limit(6).all()

    labels = []
    data = []
    for item in competences:
        c = item.Competence
        uc = item.UserCompetence
        data.append(uc.turns)
        labels.append(c.name_competence)
    return render_template('charts.html', labels = labels, data = data)


@competenceBp.route("/graphic_previous_competitions/<int:id>")
def graphicPreviousCompetitions(id):
    session = getSession()
    competence = session.query(Competence).filter(Competence.id == id).first()
    competences = session.query(Competence, UserCompetence).join(UserCompetence).filter(
        Competence.date <= competence.date,
        UserCompetence.user_id == current_user.id,
        Competence.track_id == competence.track_id
    ).limit(6).all()

    result = []
    for item in competences:
        c = item.Competence
        uc = item.UserCompetence
        result.append({
            'turns': uc.turns,
            'duration': uc.duration,
            'competence': {
                'id': c.id,
                'date': c.date.isoformat(),
                'name_competence': c.name_competence,
                'track_id': c.track_id,
                'category_id': c.category_id,
            },
        })
    return jsonify(result)



@competenceBp.route("/rendimiento")
def rendimento():
    categoria = competences.category
    return print(categoria)
