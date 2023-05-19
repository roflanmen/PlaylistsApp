import config
from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit, send
app = Flask(__name__,
            static_url_path='', 
            static_folder='../client/dist')
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'super-secret'

app.config["SQLALCHEMY_DATABASE_STR"] = "sqlite:///main.db" 
if config.is_testing:
    app.config["SQLALCHEMY_DATABASE_STR"] = 'sqlite:///test.db'

from app.views import playlists, search, user, tracks, chat
app.register_blueprint(search.search_bp)
app.register_blueprint(playlists.playlists_bp)
app.register_blueprint(user.user_bp)
app.register_blueprint(tracks.tracks_bp)


@app.route("/", defaults={'path': ''})
@app.route("/<string:path>")
@app.route("/<path:path>")
def index(path):
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')
