from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
from app.misc_utils import *
import app.models as models
import app.db as db

playlists_bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@playlists_bp.route('/', methods=['GET'])
def get_playlists():
    playlists = db.session.query(models.Playlist).filter(models.Playlist.is_public == True).all()
    return jsonify([get_playlist_by_id(playlist.id) for playlist in playlists]), 200

@playlists_bp.route('/', methods=['POST'])
def create_playlist():
    class Playlist(Schema):
        name = fields.Str(required=True)
        is_public = fields.Bool(required=True)
        owner_id = fields.Int(required=True)
    try:
        playlist = Playlist().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    if db.session.query(models.User).filter(models.User.id == playlist['owner_id']).count() == 0:
        return jsonify({'message': 'User not found'}), 404
    new_playlist = models.Playlist(name=playlist['name'], is_public=playlist['is_public'], owner_id=playlist['owner_id'])
    try:
        db.session.add(new_playlist)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error creating playlist'}), 500
    db.session.commit()
    return jsonify(get_playlist_by_id(new_playlist.id)), 201

@playlists_bp.route('/<int:playlist_id>/', methods=['GET'])
def get_playlist(playlist_id):
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    return jsonify(get_playlist_by_id(playlist.id)), 200

@playlists_bp.route('/<int:playlist_id>/', methods=['PUT'])
def update_playlist(playlist_id):
    class Playlist(Schema):
        name = fields.Str()
        is_public = fields.Bool()
    try:
        playlist = Playlist().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    playlist_to_update = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist_to_update is None:
        return jsonify({'message': 'Playlist not found'}), 404
    try:
        if playlist.__contains__('name'):
            playlist_to_update.name = playlist['name']
        if playlist.__contains__('is_public'):
            playlist_to_update.is_public = playlist['is_public']
    except:
        db.session.rollback()
        return jsonify({'message': 'Error updating playlist'}), 500
    db.session.commit()
    return jsonify(get_playlist_by_id(playlist_to_update.id)), 200

@playlists_bp.route('/<int:playlist_id>/', methods=['DELETE'])
def delete_playlist(playlist_id):
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    try:
        db.session.delete(playlist)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error deleting playlist'}), 500
    db.session.commit()
    return jsonify({'message': 'Playlist deleted'}), 200

@playlists_bp.route('/<int:playlist_id>/tracks/', methods=['GET'])
def get_playlist_tracks(playlist_id):
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    tracks = db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.playlist_id == playlist_id).all()
    return jsonify([{"title": track.title, "playlist_id": track.playlist_id, "youtube_id": track.youtube_id} for track in tracks]), 200

@playlists_bp.route('/<int:playlist_id>/tracks/', methods=['POST'])
def add_track_to_playlist(playlist_id):
    class Track(Schema):
        youtube_id = fields.Str(required=True)
    try:
        track = Track().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    for track_in_playlist in get_tracks_from_playlist(playlist_id):
        if track_in_playlist['youtube_id'] == track['youtube_id']:
            return jsonify({'message': 'Track already exists in playlist'}), 400
    track_info = get_track_info(track['youtube_id'])
    if track_info == {}:
        return jsonify({'message': 'Track not found'}), 404
    new_track = models.TracksInPlaylist(title=track_info['title'], playlist_id=playlist_id, youtube_id=track_info['youtube_id'])
    try:
        db.session.add(new_track)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error adding track to playlist'}), 500
    db.session.commit()
    return jsonify({"title": new_track.title, "playlist_id": new_track.playlist_id, "youtube_id": new_track.youtube_id}), 201

@playlists_bp.route('/<int:playlist_id>/tracks/<string:youtube_id>/', methods=['DELETE'])
def delete_track_from_playlist(playlist_id, youtube_id):
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return jsonify({'message': 'Playlist not found'}), 404
    track = db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.playlist_id == playlist_id, models.TracksInPlaylist.youtube_id == youtube_id).first()
    if track is None:
        return jsonify({'message': 'Track not found'}), 404
    try:
        db.session.delete(track)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error deleting track from playlist'}), 500
    db.session.commit()
    return jsonify({'message': 'Track deleted'}), 200