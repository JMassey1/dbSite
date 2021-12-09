from . import engine
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import text

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        pass


    if current_user.isArtist():
        with engine.connect() as conn:
            songTableP = conn.execute(
                text("SELECT Songs.songName, Albums.albumName, Songs.genre, AVG(RATES.rating) "
                     "FROM Songs, Albums, RATES, HAS, IS_ON "
                     "WHERE Songs.songID = IS_ON.songID "
                     "AND IS_ON.artistID = :artistID "
                     "AND Albums.albumID = HAS.albumID "
                     "AND HAS.songID = Songs.songID "
                     "AND RATES.songID = Songs.songID "
                     "GROUP BY Songs.songName"),
                {"artistID": current_user.get_id()}
            )
            albumTableP = conn.execute(
                text("SELECT Albums.albumName, Albums.numTracks, Albums.genre, AVG(RATES.rating) "
                     "FROM Albums, RATES, HAS, IS_ON "
                     "WHERE Albums.albumID = IS_ON.albumID "
                     "AND IS_ON.artistID = :artistID "
                     "AND RATES.albumID = Albums.albumID "
                     "GROUP BY Albums.albumName"),
                {"artistID": current_user.get_id()}
            )
            print(current_user.User_ID)
            songTable = []
            albumTable = []
            print("songTable:")
            for row in songTableP:
                songTable.append(row)
                print(row)
            print("albumTable")
            for row in albumTableP:
                albumTable.append(row)
                print(row)

    else:
        with engine.connect() as conn:
            songTableP = conn.execute(
                text("SELECT Songs.songName, Albums.albumName, Songs.genre, RATES.rating, Users.username "
                     "FROM Songs, Albums, RATES, Users, Artists, HAS, CREATES, CONTAINS, IS_ON "
                     "WHERE Songs.songID = CONTAINS.songID "
                     "AND CONTAINS.libID = CREATES.libID "
                     "AND CREATES.listenerID = :listenerID "
                     "AND Songs.songID = HAS.songID "
                     "AND HAS.albumID = Albums.albumID "
                     "AND Songs.songID = RATES.songID "
                     "AND Songs.songID = IS_ON.songID "
                     "AND IS_ON.artistID = Artists.User_ID "
                     "AND Artists.User_ID = Users.User_ID "
                     "GROUP BY Songs.songName"),
                {"listenerID": current_user.get_id()}
            )
            albumTableP = conn.execute(
                text("SELECT Albums.albumName, Albums.numTracks, Albums.genre, RATES.rating, Users.username "
                     "FROM Albums, RATES, Users, Artists, HAS, CREATES, CONTAINS, IS_ON "
                     "WHERE Albums.albumID = CONTAINS.albumID "
                     "AND CONTAINS.libID = CREATES.libID "
                     "AND CREATES.listenerID = :listenerID "
                     "AND Albums.albumID = RATES.albumID "
                     "AND Albums.albumID = IS_ON.albumID "
                     "AND IS_ON.artistID = Artists.User_ID "
                     "AND Artists.User_ID = Users.User_ID "
                     "GROUP BY Albums.albumName"),
                {"listenerID": current_user.get_id()}
            )
            print(current_user.User_ID)
            songTable = []
            albumTable = []
            print("songTable:")
            for row in songTableP:
                songTable.append(row)
                print(row)
            print("albumTable:")
            for row in albumTableP:
                albumTable.append(row)
                print(row)

    return render_template("home.html", user=current_user, songTable=songTable, albumTable=albumTable)
