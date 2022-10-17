from sqlalchemy import *
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(url='postgresql://admin:admin@localhost/pp')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_public = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)

class TracksInPlaylist(Base):
    __tablename__ = "tracks_in_playlists"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=False)
    track_youtube_id = Column(String(64), nullable=False)
