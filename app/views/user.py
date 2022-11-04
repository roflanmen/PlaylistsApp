from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from app.misc_utils import *
import app.models as models
import app.db as db

user_bp = Blueprint('user', __name__, url_prefix='/user')
bcrypt = Bcrypt()

@user_bp.route('/', methods=['POST'])
def create_user():
    class User(Schema):
        username = fields.Str(required=True)
        password = fields.Str(required=True)
    try:
        user = User().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    if db.session.query(models.User).filter(models.User.username == user['username']).count() != 0:
        return jsonify({'message': 'User already exists'}), 400

    new_user = models.User(username=user['username'], password=bcrypt.generate_password_hash(user['password']).decode('utf-8'))
    try:
        db.session.add(new_user)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error creating user'}), 500
    db.session.commit()
    return get_user(new_user.id)[0], 201

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    res = {'id': user.id, 'username': user.username, 'playlists': []}
    for playlist in db.session.query(models.Playlist).filter(models.Playlist.owner_id == user_id).all():
        res['playlists'].append(get_playlist_by_id(playlist.id))
    return jsonify(res), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    class User(Schema):
        username = fields.Str()
        password = fields.Str(required=True)
        new_password = fields.Str()
    try:
        user = User().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    user_to_update = db.session.query(models.User).filter(models.User.id == user_id).first()
    if user_to_update is None:
        return jsonify({'message': 'User not found'}), 404
    if not bcrypt.check_password_hash(user_to_update.password, user['password']):
        return jsonify({'message': 'Incorrect password'}), 400
    try:
        if user.__contains__('username'):
            user_to_update.username = user['username']
        if user.__contains__('new_password'):
            user_to_update.password = bcrypt.generate_password_hash(user['new_password']).decode('utf-8')
    except:
        db.session.rollback()
        return jsonify({'message': 'Error updating user'}), 500
    db.session.commit()
    return get_user(user_id)[0], 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    try:
        db.session.delete(user)
    except:
        db.session.rollback()
        return jsonify({'message': 'Error deleting user'}), 500
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200