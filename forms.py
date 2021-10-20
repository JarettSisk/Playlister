"""Forms for playlist app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class UserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Playlist name", validators=[InputRequired()])
    description = StringField("Playlist description", validators=[InputRequired()])

class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Song title", validators=[InputRequired()])
    artist = StringField("Artist name", validators=[InputRequired()])
