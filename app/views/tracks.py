from flask import Blueprint, jsonify
from app.misc_utils import get_track_info

tracks_bp = Blueprint('tracks', __name__, url_prefix='/api/tracks')

@tracks_bp.route('/<string:track_id>/', methods=['GET'])
def get_track(track_id):
    res = get_track_info(track_id)
    if res is None:
        return jsonify({'message': 'Track not found'}), 404
    return jsonify(res), 200