from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from sqlalchemy import func
from app.misc_utils import *
import app.models as models
import app.db as db
from pytube import Search
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity
)

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

@search_bp.route('/tracks/', methods=['GET'])
def search_tracks():
    res = []
    tracks = 10
    for result in Search(request.args['query']).results:
        res.append({"title": result.title, "youtube_id": result.video_id})
    return jsonify(res[:tracks]), 200

@search_bp.route('/users/', methods=['GET'])
def search_users():
    users = db.session.query(models.User).filter(models.User.username.like('%' + request.args['query'] + '%')).all()
    res = []
    for user in users:
        res.append({'id': user.id, 'username': user.username})
    return jsonify(res), 200

@search_bp.route('/playlists/', methods=['GET'])
@jwt_required(optional=True)
def search_playlists():
    if is_admin(get_jwt_identity()):
        playlists = db.session.query(models.Playlist).\
                    filter(models.Playlist.name.like('%' + request.args['query'] + '%')).all()
    else:
        playlists = db.session.query(models.Playlist).\
                    filter(models.Playlist.name.like('%' + request.args['query'] + '%'), 
                           models.Playlist.is_public == True).all()
    res = []
    for playlist in playlists:
        res.append(get_playlist_by_id(playlist.id))
    return jsonify(res), 200
