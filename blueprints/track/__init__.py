from aws import getFile
from botocore.retries import bucket
from blueprints.training import trainings
import uuid
import os
from flask_login.utils import login_required
from sqlalchemy.sql import text
from flask import render_template, request, jsonify
from flask.blueprints import Blueprint

from flask.helpers import make_response, url_for
from werkzeug.utils import secure_filename

from database import getSession
from utils import query_to_dict
from utils.uploadFiles import uploadfiles
from models import Track, TrackImage, Competence
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
    tracks = session.query(Track).outerjoin(TrackImage).all()
    return render_template('tracks.html', tracks=tracks)


@trackBp.route("/createTracks")
@login_required
def createTracks():
    return render_template('createTracks.html')


@trackBp.route("/cronometro")
@login_required
def cronometro():
    return render_template('cronometro.html')


@trackBp.route("/indextra")
@login_required
def indextra():
    return render_template('indextra.html')


folderTracks = 'tracks/'
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
        imagesPaths = uploadfiles(files, folderTracks)
        for imagesPath in imagesPaths:
            trackImage = TrackImage()
            trackImage.src = imagesPath
            trackImage.track_id = track.id
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


@ trackBp.route("/track_image/<src>")
@login_required
def imageTrack(src):
    file = getFile(folderTracks + src)
    response = make_response(file['Body'].read())
    response.headers['Content-Type'] = 'image/jpg'
    return response
