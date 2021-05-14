from database import getSession
from flask_login import current_user
from models import Competence, Training, Track, Category, UserCompetence
from . import getPerformance, getPerformanceCompetence


def dataChartTrainings():
    session = getSession()
    query = session.query(Training, Track, Category).join(
        Track, Category
    ).filter(Training.user_id == current_user.id)
    query = query.order_by(Training.date.desc())
    query = query.limit(10)
    trainings = query.all()
    labels = []
    data = []
    for training in trainings:
        performance = getPerformance(
            training.Training, training.Track, training.Category,)
        date = training.Training.date
        start_time = training.Training.start_time
        labels.append(date.strftime("%d-%b-%Y") +
                      (start_time.strftime(" %H:%M") if start_time else ""))
        data.append(performance)
    return labels, data


def dataChartCompetences():
    session = getSession()
    competences = session.query(Competence, Track, UserCompetence, Category).join(Track, UserCompetence, Category).filter(
        UserCompetence.user_id == current_user.id, UserCompetence.turns.isnot(
            None), UserCompetence.duration.isnot(None)
    ).limit(8).all()
    labels = []
    data = []
    for item in competences:
        performance = getPerformanceCompetence(
            item.Competence, item.Track, item.Category, item.UserCompetence
        )
        data.append(performance)
        labels.append(item.Competence.name_competence)
    return labels, data
