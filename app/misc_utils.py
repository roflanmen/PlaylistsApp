from pytube import YouTube
import app.models as models
import app.db as db

def get_playlist_by_id(playlist_id: int) -> dict:
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    res = {"id": playlist.id, "name": playlist.name, "is_public": playlist.is_public, "owner_id": playlist.owner_id, "tracks": get_tracks_from_playlist(playlist.id)}
    return res

def get_tracks_from_playlist(playlist_id: int) -> list:
    tracks = db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.playlist_id == playlist_id).all()
    return [{"title": track.title, "youtube_id": track.youtube_id} for track in tracks]

def get_track_info(track_id: str) -> dict:
    try:
        video = YouTube('https://www.youtube.com/watch?v=' + track_id)
        res = {'title': video.title, 'youtube_id': track_id}
    except:
        return
    return res

def get_entry(Class, id):
    entry = db.session.query(Class).filter(Class.id == id).first()
    if entry is None:
        return
    return entry

def create_entry(Class, **kwargs):
    entry = Class(**kwargs)
    db.session.add(entry)
    db.session.commit()
    return entry

def update_entry(Class, id, **kwargs):
    entry = db.session.query(Class).filter(Class.id == id).first()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    db.session.commit()
    return entry

def delete_entry(Class, id):
    entry = db.session.query(Class).filter(Class.id == id).first()
    if entry is None:
        return
    db.session.delete(entry)
    db.session.commit()
    return entry

def is_admin(id):
    user = get_entry(models.User, id)
    if user is None:
        return False
    return user.is_admin