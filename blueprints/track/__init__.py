import uuid
import os
from flask_login.utils import login_required
from sqlalchemy.sql import text
from flask import render_template, request, jsonify
from flask.blueprints import Blueprint

from flask.helpers import url_for
from werkzeug.utils import secure_filename

from database import getSession
from utils import query_to_dict
from models import Track, TrackImage
from flask import redirect

trackBp = Blueprint(
    'track',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/track'
)


@trackBp.route("/tracks")
@login_required
def tracks():

    session = getSession()
    connection = session.connection()
    results = connection.execute('SELECT * FROM tracks')
    tracks = query_to_dict(results)
    return render_template('tracks.html', tracks=tracks)


@trackBp.route("/createTracks")
@login_required
def createTracks():
    return render_template('createTracks.html')


folderTracks = 'static/tracks/'
if not os.path.exists(folderTracks):
    os.makedirs(folderTracks)


@trackBp.route("/createTracks", methods=['POST'])
@login_required
def createPost():
    session = getSession()
    name = request.form.get('name')
    location = request.form.get('location')
    size = request.form.get('size')
    try:
        """  connection.execute(
            "INSERT INTO tracks(name,location,size) VALUES(%s, %s,%s)",
            name, location, size
        ) """
        track = Track()
        track.name = name
        track.location = location
        track.size = size
        session.add(track)
        session.commit()

        files = request.files.getlist("images")
        for file in files:
            key = uuid.uuid4().hex
            ext = os.path.splitext(file.filename)[1]
            newName = key+ext
            trackImage = TrackImage()
            trackImage.src = newName
            trackImage.track_id = track.id
            file.save(folderTracks + newName)
            session.add(trackImage)
        session.commit()
        return redirect(url_for('track.tracks'))
    except Exception as error:
        session.rollback()
        raise error
    return render_template('createTracks.html')


@ trackBp.route("/track/delete/<int:id>")
@login_required
def delete(id):
    session = getSession()
    track = session.query(Track).filter(Track.id == id)
    track.delete()
    session.commit()
    return redirect(url_for('track.tracks'))
