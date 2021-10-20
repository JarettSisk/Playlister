"""SQLAlchemy models for Playlister."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    # sqlalchemy relationship for easy querying
    playlists = db.relationship('Playlist')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False    


class Playlist(db.Model):
    """Playlist Model"""
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Through relationship
    songs = db.relationship('Song', secondary='playlists_songs', cascade="all, delete", backref="playlists" )
    
    # Foriegn key to only show playlists made by this user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Song(db.Model):
    """Song Model"""
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.String, nullable=False)



class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    __tablename__ = 'playlists_songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"))
