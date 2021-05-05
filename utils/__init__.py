from database import getSession
from flask.globals import session
from models import Category, Track, Training


def query_to_dict(ret):
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return []


def getPerformance(training: Training, track: Track = None, category: Category = None):
    session = getSession()
    if not track:
        track = session.query(Track).get(training.track_id)
    if not category:
        category = session.query(Category).get(training.category_id)
    size = int(track.size) / 1000
    turns = (7 / (size * 60)) / (1 / (3 * category.duration_max))
    return (training.turns * 100) / turns