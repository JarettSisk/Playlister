import os
from flask import Flask, render_template, redirect, session, flash, request, jsonify
from flask.helpers import url_for
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Playlist, Song, PlaylistSong
from forms import UserForm, SongForm, PlaylistForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///playlister_database")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'secret1234321')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """ Home page route """
    if 'user_id' not in session:
        return render_template('index.html')

    return redirect(f"/user/{session['user_id']}")

@app.route('/user/<int:user_id>')
def show_playlists(user_id):
    """ Show the user and the list of playlists they have made"""
    
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    user = User.query.get_or_404(user_id)

    if user:
        return render_template("playlists.html", user=user)
    
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ Log in the user """
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Autheniticate the users credentials
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect(f"/user/{user.id}")
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """ Register in the user """
    form = UserForm()
    if form.validate_on_submit():
        # Saving the form data
        username = form.username.data
        password = form.password.data

        # Register the user and handle integegrity errors
        user = User.register(User, username, password)
        try:
            # Create the new user and add to the DB
            new_user = User(username = user.username, password = user.password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            form.username.errors = ['Invalid username/password.']
            return render_template('register.html', form=form)

        # Fetch the new user from DB
        user = User.query.get_or_404(new_user.id)
        # If found, add users id to the session
        if user:
            session['user_id'] = user.id
            return redirect(f"/user/{user.id}")
        else:
            form.username.errors = ['Invalid username/password.']
            
    # Get the register page
    return render_template('register.html', form=form)

@app.route('/logout')
def logout_user():
    """ Log out the user """
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/playlist/<int:playlist_id>', methods=['GET'])
def show_playlist(playlist_id):
    """ Show the playlist and all of the songs within the playlist."""
    user = User.query.get_or_404(session['user_id'])
    playlist = Playlist.query.get_or_404(playlist_id)

    if user:
        return render_template('playlist.html', user=user, playlist=playlist)

@app.route('/playlist/<int:playlist_id>/songs', methods=[ 'GET'])
def get_songs(playlist_id):
    """ Get all the songs related to the playlist """
    playlist = Playlist.query.get_or_404(playlist_id)
    all_songs = [song.serialize() for song in playlist.songs]
    return jsonify(songs=all_songs)
        


@app.route('/playlist/<int:playlist_id>/add-song', methods=[ 'POST'])
def add_song(playlist_id):
    """ Add a new song to the playlist """
    playlist = Playlist.query.get_or_404(playlist_id)
    data = request.json
    title = data['title']
    artist = data['artist']
    new_song = Song(title=title, artist=artist)
    db.session.add(new_song)
    db.session.commit()

    # Adding to the M2M table
    playlist_song = PlaylistSong(
    playlist_id = playlist.id,
    song_id = new_song.id
    )
    db.session.add(playlist_song)
    db.session.commit()
    
    data = {
        "title": new_song.title,
        "artist": new_song.artist,
        "song_id": new_song.id }

    return (jsonify(data), 201)

@app.route('/playlist/<int:playlist_id>/remove-song', methods=['POST'])
def remove_song(playlist_id):
    """ Remove a new song to the playlist """
    data = request.json
    song = Song.query.get_or_404(data['song_id'])
    if song:

        db.session.delete(song)
        db.session.commit()

        return ("Song sucessfully Deleted", 200)

    return ('Oop. Something went wrong')


@app.route('/playlist/add', methods=['GET', 'POST'])
def creat_new_playlist():
    """ Add a new playlist"""
    # Checking for logged in user
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    # Get the user
    user = User.query.get_or_404(session['user_id'])
 
    form = PlaylistForm()
    """ Form for adding new playlists """
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        new_playlist = Playlist(name=name, description=description, user_id=user.id)
        db.session.add(new_playlist)
        db.session.commit()
        # Redirect back to playlists
        return redirect(f"/user/{user.id}")

    return render_template('new-playlist.html', form=form, user=user)

@app.route('/playlist/<int:playlist_id>/remove', methods=['POST'])
def remove_playlist(playlist_id):
    """ Delete the playlist """
    # Checking for logged in user
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        flash('Playlist deleted')

    return redirect("/")

@app.route('/faq')
def show_faq_page():
    user = User.query.get_or_404(session['user_id'])
    return render_template('faq.html', user=user)


