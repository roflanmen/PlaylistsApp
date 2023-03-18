import config
from flask import Flask
app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'super-secret'

app.config["SQLALCHEMY_DATABASE_STR"] = "sqlite:///main.db" 
if config.is_testing:
    app.config["SQLALCHEMY_DATABASE_STR"] = 'sqlite:///test.db'

from app.views import playlists, search, user, tracks 
app.register_blueprint(search.search_bp)
app.register_blueprint(playlists.playlists_bp)
app.register_blueprint(user.user_bp)
app.register_blueprint(tracks.tracks_bp)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path>')
def static_proxy(path):
    return app.send_static_file(path)