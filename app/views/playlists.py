from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from app.misc_utils import *
import app.models as models
import app.db as db
from app.schemas import *
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity
)
jwt = JWTManager(app)
playlists_bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@playlists_bp.route('/', methods=['GET'])
def get_playlists():
    playlists = db.session.query(models.Playlist).filter(models.Playlist.is_public == True).all()
    return jsonify([get_playlist_by_id(playlist.id) for playlist in playlists]), 200

@playlists_bp.route('/', methods=['POST'])
@jwt_required()
def create_playlist():
    try:
        playlist = PlaylistToCreate().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    if get_entry(models.User, get_jwt_identity()) is None:
        return jsonify({'message': 'User not found'}), 404

    new_playlist = create_entry(models.Playlist, **playlist, owner_id=get_jwt_identity())
    return jsonify(get_playlist_by_id(new_playlist.id)), 201

@playlists_bp.route('/<int:playlist_id>/', methods=['GET'])
@jwt_required(optional=True)
def get_playlist(playlist_id):
    playlist = get_entry(models.Playlist, playlist_id)
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    if not playlist.is_public:
        if get_jwt_identity() is None:
            return jsonify({'message': 'Unauthorized'}), 401
        if get_jwt_identity() != playlist.owner_id:
            return jsonify({'message': 'Forbidden'}), 403
    return jsonify(get_playlist_by_id(playlist.id)), 200

@playlists_bp.route('/<int:playlist_id>/', methods=['PUT'])
@jwt_required()
def update_playlist(playlist_id):
    try:
        playlist = PlaylistToUpdate().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    db_playlist = get_entry(models.Playlist, playlist_id)
    if db_playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    if get_jwt_identity() != db_playlist.owner_id:
        return jsonify({'message': 'Forbidden'}), 403
    update_entry(models.Playlist, playlist_id, **playlist)
    return jsonify(get_playlist_by_id(playlist_id)), 200

@playlists_bp.route('/<int:playlist_id>/', methods=['DELETE'])
@jwt_required()
def delete_playlist(playlist_id):
    playlist = get_entry(models.Playlist, playlist_id)
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    if get_jwt_identity() != playlist.owner_id:
        return jsonify({'message': 'Forbidden'}), 403
    delete_entry(models.Playlist, playlist_id)
    return jsonify({'message': 'Playlist deleted'}), 200

@playlists_bp.route('/<int:playlist_id>/tracks/', methods=['POST'])
@jwt_required()
def add_track_to_playlist(playlist_id):
    try:
        track = TrackToCreate().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    playlist = get_entry(models.Playlist, playlist_id)
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    
    if get_jwt_identity() != playlist.owner_id:
        return jsonify({'message': 'Forbidden'}), 403

    if db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.youtube_id == track['youtube_id'], models.TracksInPlaylist.playlist_id == playlist_id).count() != 0:
        return jsonify({'message': 'Track already exists in playlist'}), 400
    
    track_info = get_track_info(track['youtube_id'])
    if track_info is None:
        return jsonify({'message': 'Track not found'}), 404

    create_entry(models.TracksInPlaylist, **track_info, playlist_id=playlist_id)

    return jsonify(get_playlist_by_id(playlist_id)), 201

@playlists_bp.route('/<int:playlist_id>/tracks/<string:youtube_id>/', methods=['DELETE'])
@jwt_required()
def delete_track_from_playlist(playlist_id, youtube_id):
    playlist = get_entry(models.Playlist, playlist_id)
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    if playlist.owner_id != get_jwt_identity():
        return jsonify({'message': 'Forbidden'}), 403
    track = db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.playlist_id == playlist_id, models.TracksInPlaylist.youtube_id == youtube_id).first()
    if track is None:
        return jsonify({'message': 'Track not found'}), 404
    db.session.delete(track)
    db.session.commit()
    return jsonify({'message': 'Track deleted'}), 200