from sqlalchemy.sql.expression import null, or_
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from models.CategoryAge import CategoryAge
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


@trainingBp.route("/trainings", methods=['GET'])
@login_required
def trainings():

    session = getSession()
    trainings = session.query(Training, Track, Category).join(
        Track, Category
    ).filter(Training.user_id == current_user.id).order_by(Training.date.desc()).limit(10).all()
    return render_template('trainings.html', trainings=trainings)


@trainingBp.route("/trainingsAll", methods=['GET'])
@login_required
def trainingsAll():
    page = 1
    limit = 10
    getArg = request.args.get
    try:
        page = int(getArg('page'))
    except:
        pass
    try:
        limit = int(getArg('limit'))
    except:
        pass
    session = getSession()
    query = session.query(Training, Track, Category).join(
        Track, Category
    ).filter(Training.user_id == current_user.id)
    query = query.order_by(Training.date.desc())
    count = query.count()
    query = query.offset((page * limit) - limit)

    query = query.limit(limit)

    trainings = query.all()
    return render_template('trainings_all.html', trainings=trainings, count=count, page=page, limit=limit)


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
    age = current_user.getYearsOld()
    categories = session.query(Category).join(CategoryAge).filter(
        or_(CategoryAge.since <= age, CategoryAge.until <= age)
    ).all()

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
