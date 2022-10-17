from models import *

session = Session()

user = User(name='Dungeon', password='master')
playlist = Playlist(name='Van', is_public=True, owner_id=1)
tracks_in_playlist = TracksInPlaylist(name="Will be ok", playlist_id=1, track_youtube_id="asdsad")

session.add(user)
session.commit()

session.add(playlist)
session.commit()

session.add(tracks_in_playlist)
session.commit()

print(session.query(User).all()[0].name)