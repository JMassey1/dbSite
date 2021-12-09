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
                #text("SELECT Songs.songName, Albums.albumName, Songs.genre, AVG(RATES.rating) "
                #     "FROM Songs, Albums, RATES, HAS, IS_ON "
                #     "WHERE Songs.songID = IS_ON.songID "
                #     "AND IS_ON.artistID = :artistID "
                #     "AND Albums.albumID = HAS.albumID "
                #     "AND HAS.songID = Songs.songID "
                #     "AND RATES.songID = Songs.songID "
                #     "GROUP BY Songs.songName"),
                #{"artistID": current_user.get_id()}
                text("SELECT Songs.songName FROM Songs, IS_ON WHERE "
                     "Songs.songID = IS_ON.songID "
                     "AND IS_ON.artistID = :artistID"),
                {"artistID": current_user.get_id()}
            )
            print(songTable.first())
    else:
        songTable = []

    return render_template("home.html", user=current_user, table=songTable)
