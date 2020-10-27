"""Script to run a Chat App"""
# pylint: disable=no-member
# pylint: disable=no-else-return
# pylint: disable=too-many-branches
# pylint: disable=redefined-outer-name
#pylint: disable=global-statement
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask_socketio
import flask_sqlalchemy
from googletrans import Translator
import requests
import flask
from flask import request


dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

app = flask.Flask(__name__)
db = flask_sqlalchemy.SQLAlchemy()


def init_db(app):
    """Initialize app"""
    database_uri = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)
    db.app = app
    db.create_all()
    db.session.commit()
import chatDB
translator = Translator()

# Initializing
app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


def bot_response_about_help(function):
    """Run Bot's help and about commands"""
    if function[0] == "help":
        return ("Type either: \n1)!! translate/funtranslate {text}\n2)!! tamil-translate {text}\n"
                    "3)!! random-fact\n4)!! text-to-binary {text}\n5)!! help\n6)!! about")
    else:
        return "I am a bot, I will respond to messages that start with !!"


def bot_response_api(string):
    """Run Bot's Commands"""
    ret_str = "Command not found"
    string = string[3:]
    #!! translate/funtranslate, about, help
    function = string.split(" ", 1)
    if function[0] == "about" or function[0] == "help":
        ret_str = bot_response_about_help(function)
    elif function[0] == "translate" or function[0] == "funtranslate":
        if len(function) == 1 or function[1] == "":
            ret_str = "Error: text not given"
        else:
            payload = {"text": function[1]}
            ret_str = requests.get(
                "https://api.funtranslations.com/translate/yoda.json", params=payload
            ).json()
            if "error" not in ret_str:
                ret_str = ret_str["contents"]["translated"]
            else:
                ret_str = "Error: Translate limit hit: try in an hour"

    elif function[0] == "tamil-translate":
        if len(function) == 1 or function[1] == "":
            ret_str = "Error: text not given"
        else:
            ret_str = translator.translate(function[1], src="en", dest="ta").text

    elif function[0] == "random-fact":
        ret_str = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en"
        ).json()["text"]

    elif function[0] == "text-to-binary":
        if len(function) == 1 or function[1] == "":
            ret_str = "Error: text not given"
        else:
            payload = {"text": function[1]}
            ret_str = requests.get(
                "https://some-random-api.ml/binary", params=payload
            ).json()["binary"]

    return ret_str


# Emits the select * database query
def emit_all_from_database(channel, sid):
    """Select all from databse"""
    print(sid)
    all_messages = [
        db_message.message for db_message in db.session.query(chatDB.chatmessages).all()
    ]
    print(all_messages)
    socketio.emit(channel, {"text": all_messages}, sid)


def add_to_db_and_emit(text):
    """Add to databse and emit to react components"""
    print(chatDB.chatmessages(text))
    db.session.add(chatDB.chatmessages(text))
    db.session.commit()


@app.route("/")
def hello():
    """Render HTML"""
    return flask.render_template("index.html")


COUNT = 0


@socketio.on("connect")
def on_connect():
    """On connect update count"""
    global COUNT
    COUNT += 1
    print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    """On disconnect update count"""
    global COUNT
    COUNT -= 1
    print("Someone disconnected!")
    socketio.emit("connection", {"connection": COUNT})


USERNAME = ""


@socketio.on("new google user")
def on_new_google_user(data):
    """On new google user get username and load page and count"""
    sid = request.sid
    print("Got an event for new google user input with data:", data)
    global USERNAME
    USERNAME = data["name"]
    socketio.emit("google user", {"username": USERNAME}, sid)
    socketio.emit("connection", {"connection": COUNT})
    socketio.emit("chatArea", {"uname": USERNAME}, sid)
    print("connection status sent to user")
    # push_new_user_to_db(data['name'], models.AuthUserType.GOOGLE)
    emit_all_from_database("text received", sid)


@socketio.on("new message")
def on_new_data(data):
    """Parse messages for bot command and update database"""
    print("Got an event for data:", data)
    message = data["new message"]
    global USERNAME
    if message != "":
        msg = USERNAME + ": " + message
        add_to_db_and_emit(msg)

    socketio.emit("text received", {"text": msg})
    if message[0:2] == "!!":
        bot_response = bot_response_api(message)
        add_to_db_and_emit("Bot: " + bot_response)
        socketio.emit("text received", {"text": "Bot: " + bot_response})


if __name__ == "__main__":
    print(app)
    init_db(app)
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
