from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from app.misc_utils import *
import app.models as models
import app.db as db
from pytube import Search

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/tracks/', methods=['GET'])
def search_tracks():
    res = []
    for result in Search(request.args['query']).results:
        res.append({'title': result.title, 'id': result.video_id})
    return jsonify(res), 200

@search_bp.route('/users/', methods=['GET'])
def search_users():
    users = db.session.query(models.User).filter(models.User.name.like('%' + request.args['query'] + '%')).all()
    res = []
    for user in users:
        res.append({'id': user.id, 'name': user.name, 'playlists': []})
        for playlist in db.session.query(models.Playlist).filter(models.Playlist.owner_id == user.id).all():
            res[-1]['playlists'].append(get_playlist_by_id(playlist.id))
    return jsonify(res), 200

@search_bp.route('/playlists/', methods=['GET'])
def search_playlists():
    playlists = db.session.query(models.Playlist).filter(models.Playlist.name.like('%' + request.args['query'] + '%')).all()
    res = []
    for playlist in playlists:
        res.append(get_playlist_by_id(playlist.id))
    return jsonify(res), 200