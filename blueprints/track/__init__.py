from flask import render_template, request, jsonify
from flask.blueprints import Blueprint

from database import getSession
from utils import query_to_dict
from models.Track import Track

trackBp = Blueprint(
    'track',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/track'
)


@trackBp.route("/tracks")
def tracks():

    session = getSession()
    connection = session.connection()
    results = connection.execute('SELECT * FROM tracks')
    tracks = query_to_dict(results)
    return render_template('tracks.html', tracks=tracks)


@trackBp.route("/createTracks", methods=['GET', 'POST'])
def createTracks():
    method = request.method
    if(method == 'POST'):
        name = request.form.get('name')
        ubiety = request.form.get('location')
        size = request.form.get('size')
        session = getSession()
        connection = session.connection()
        try:
            connection.execute(
                "INSERT INTO tracks(name,location,size) VALUES(%s, %s,%s)",
                name, ubiety, size
            )
            session.commit()
            return "Data saved"
        except Exception as error:
            session.rollback()
            raise error
    return render_template('createTracks.html')
