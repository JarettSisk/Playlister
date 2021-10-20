""" Test data for playlister application"""
from re import U
from app import app
from models import db, User, Playlist, Song, PlaylistSong


db.drop_all()
db.create_all()
registered_user1 = User.register(User, "testuser1", 'testpassword1')
test_user1 = User(
    username = registered_user1.username,
    password = registered_user1.password
)

registered_user2 = User.register(User, "testuser2", 'testpassword2')
test_user2 = User(
    username = registered_user2.username,
    password = registered_user2.password
)

db.session.add_all([test_user1, test_user2])
db.session.commit()


test_playlist1 = Playlist(
    name = 'My birthday playlist',
    description = 'An epic playlist for my birthday!',
    user_id = test_user1.id
)

test_playlist2 = Playlist(
    name = 'My wedding playlist',
    description = 'An epic playlist for my wedding!',
    user_id = test_user2.id
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
db.session.add_all([test_playlist1, test_playlist2, test_song1, test_song2])
db.session.commit()


test_playlist_song1 = PlaylistSong(
    playlist_id = test_playlist1.id,
    song_id = test_song1.id
)

test_playlist_song2 = PlaylistSong(
    playlist_id = test_playlist2.id,
    song_id = test_song2.id
)

db.session.add_all([test_playlist_song1, test_playlist_song2])
db.session.commit()