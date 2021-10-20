import re
from flask import Flask, render_template, redirect, session, flash
from flask.helpers import url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Playlist, Song, PlaylistSong
from forms import UserForm, SongForm, PlaylistForm
# from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///playlister_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """ Home page route """
    if 'user_id' not in session:
        return render_template('index.html')

    return redirect('/user')

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

@app.route('/logout')
def logout_user():
    """ Log out the user """
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/playlist/<int:playlist_id>', methods=['GET', 'POST'])
def show_playlist(playlist_id):
    """ Show the playlist and all of the songs within the playlist. Also a form to add more songs """
    user = User.query.get_or_404(session['user_id'])
    playlist = Playlist.query.get_or_404(playlist_id)

    if user:
        form = SongForm()
        if form.validate_on_submit():
            title = form.title.data
            artist = form.artist.data
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

            return redirect(f"/playlist/{playlist_id}")

    return render_template('playlist.html', user=user, playlist=playlist, form=form)

@app.route('/playlist/add', methods=['GET', 'POST'])
def creat_new_playlist():
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
