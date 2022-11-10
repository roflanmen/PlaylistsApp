from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

from app.views import playlists, search, user, tracks

app.register_blueprint(search.search_bp)
app.register_blueprint(playlists.playlists_bp)
app.register_blueprint(user.user_bp)
app.register_blueprint(tracks.tracks_bp)