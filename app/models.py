from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref

Base = declarative_base()

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_public = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", backref=backref("playlists", passive_deletes=True))

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    username = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    # Admin can view all playlists, edit and delete them

class TracksInPlaylist(Base):
    __tablename__ = "tracks_in_playlists"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    playlist_id = Column(Integer, ForeignKey('playlists.id', ondelete='CASCADE'), nullable=False)
    youtube_id = Column(String(64), nullable=False)
    playlist = relationship("Playlist", backref=backref("tracks_in_playlists", passive_deletes=True))
