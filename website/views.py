from . import engine
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import text

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():

    if current_user.isArtist():
        with engine.connect() as conn:
            songTable = conn.execute(
                text("SELECT Songs.songName FROM Songs WHERE username = :username"),
                {"username": username}
            )
            print(songTable.first())
    else:
        songTable = []

    return render_template("home.html", user=current_user, table=songTable)
