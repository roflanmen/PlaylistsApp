from pytube import YouTube
import app.models as models
import app.db as db

def get_playlist_by_id(playlist_id: int) -> dict:
    playlist = db.session.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if playlist is None:
        return {}
    res = {"id": playlist.id, "name": playlist.name, "is_public": playlist.is_public, "owner_id": playlist.owner_id, "tracks": get_tracks_from_playlist(playlist.id)}
    return res

def get_tracks_from_playlist(playlist_id: int) -> list:
    tracks = db.session.query(models.TracksInPlaylist).filter(models.TracksInPlaylist.playlist_id == playlist_id).all()
    return [{"id": track.id, "title": track.title, "playlist_id": track.playlist_id, "youtube_id": track.youtube_id} for track in tracks]

def get_track_info(track_id: str) -> dict:
    try:
        video = YouTube('https://www.youtube.com/watch?v=' + track_id)
        res = {'title': video.title, 'youtube_id': track_id}
    except:
        return {}
    return res