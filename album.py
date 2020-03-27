# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
    pass

class AlreadyExists(Error):
    pass


class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER,primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(year, artist, genre, album):
    assert isinstance(year, int), "Incorrect date"
    assert isinstance(artist, str), "Incorrect artist"
    assert isinstance(genre, str), "Incorrect genre"
    assert isinstance(album, str), "Incorrect album"
    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists("Такой альбом уже существет #{}".format(saved_album.id))
    
    album = Album(
            year = year,
            artist = artist,
            genre = genre,
            album = album)
    
    session.add(album)
    session.commit()
    return album

                            
        



