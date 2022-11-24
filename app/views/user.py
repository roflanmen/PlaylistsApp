from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from app.misc_utils import *
import app.models as models
import app.db as db
from app.schemas import *
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
jwt = JWTManager(app)

user_bp = Blueprint('user', __name__, url_prefix='/user')
bcrypt = Bcrypt()

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        user = UserToCreate().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    if db.session.query(models.User).filter(models.User.username == user['username']).count() != 0:
        return jsonify({'message': 'User already exists'}), 400
    user['password'] = bcrypt.generate_password_hash(user['password']).decode('utf-8')

    new_user = create_entry(models.User, **user)
    return get_user(new_user.id)[0], 201

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_me():
    return get_user(get_jwt_identity())

@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        user = UserToUpdate().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    user_id = get_jwt_identity()
    user_to_update = get_entry(models.User, user_id)
    if user_to_update is None:
        return jsonify({'message': 'User not found'}), 404
    if not bcrypt.check_password_hash(user_to_update.password, user['password']):
        return jsonify({'message': 'Incorrect password'}), 400

    if user.__contains__('username'):
        if db.session.query(models.User).filter(models.User.username == user['username']).count() != 0 and user['username'] != user_to_update.username:
            return jsonify({'message': 'User already exists'}), 400
        user_to_update.username = user['username']
    if user.__contains__('new_password'):
        user_to_update.password = bcrypt.generate_password_hash(user['new_password']).decode('utf-8')

    db.session.commit()
    return get_user(user_id)

@user_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_user():
    if delete_entry(models.User, get_jwt_identity()) is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        user = UserToLogin().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    db_user = db.session.query(models.User).filter(models.User.username == user['username']).first()
    if db_user is None:
        return jsonify({'message': 'User not found'}), 404
    if not bcrypt.check_password_hash(db_user.password, user['password']):
        return jsonify({'message': 'Incorrect password'}), 400
    access_token = create_access_token(identity=db_user.id)
    return jsonify({'token': access_token}), 200


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out'}), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required(optional=True)
def get_user(user_id):
    user = get_entry(models.User, user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    playlists = db.session.query(models.Playlist).filter(
        models.Playlist.owner_id == user_id
    ).all() if ((get_jwt_identity() == user_id)) else db.session.query(models.Playlist).filter(
        models.Playlist.owner_id == user_id,
        models.Playlist.is_public == True
    ).all()

    res = {'id': user.id, 'username': user.username, 'playlists': []}
    for playlist in playlists:
        res['playlists'].append(get_playlist_by_id(playlist.id))
    return jsonify(res), 200
