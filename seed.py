""" Test data for playlister application"""
from app import app
from models import db, User, Playlist, Song, PlaylistSong


db.drop_all()
db.create_all()

test_user = User(
    username = 'testuser1',
    password = 'TestPassword'
)

db.session.add_all([test_user])
db.session.commit()


test_playlist = Playlist(
    name = 'My birthday playlist',
    description = 'An epic playlist for my birthday!',
    user_id = test_user.id
)

test_song1 = Song(
    title = 'Rockstar',
    artist = 'Post Malone'
)

test_song2 = Song(
    title = 'Thriller',
    artist = 'Michael Jackson'
)

# Add the songs and the playlistst
db.session.add_all([test_playlist, test_song1, test_song2])
db.session.commit()


test_playlist_song = PlaylistSong(
    playlist_id = test_playlist.id,
    song_id = test_song1.id
)

db.session.add_all([test_playlist_song])
db.session.commit()