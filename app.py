from os.path import join, dirname
import flask
app = flask.Flask(__name__)
import os
import flask_sqlalchemy
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)
#Initializing database
database_uri = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

import flask_socketio

import flask_socketio
import chatDB
import random
from flask import request
import requests
import json
from googletrans import Translator
translator = Translator()
 
#Initializing
app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")



 
def bot_response_about_help(function):
    if function[0] == "help":
        return("Type either: \n1)!! translate/funtranslate {text}\n2)!! tamil-translate {text}\n3)!! random-fact\n4)!! text-to-binary {text}\n5)!! help\n6)!! about")
    else:
        return("I am a bot, I will respond to messages that start with !!") 
    
def bot_response_api(string):
    ret_str = "Command not found"
    string = string[3:]
    #!! translate/funtranslate, about, help
    function = string.split(" ",1)
    if function[0] == "about" or function[0] == "help":
        ret_str = bot_response_about_help(function)
    elif function[0] == "translate" or function[0] == "funtranslate":
        if len(function) == 1 or function[1] == "":
            ret_str = "Error: text not given"
        else:
            payload = {'text': function[1]}
            ret_str = requests.get('https://api.funtranslations.com/translate/yoda.json', params=payload).json()
    #         r = {
    #     "success": {
    #         "total": 1
    #     },
    #     "contents": {
    #         "translated": "Lost a planet,  master obiwan has.",
    #         "text": "Master Obiwan has lost a planet.",
    #         "translation": "yoda"
    #     }
    # }
            if "error" not in ret_str:
                ret_str = ret_str['contents']['translated']
            else:
                ret_str = "Error: Translate limit hit: try in an hour"
            
    elif function[0] == "tamil-translate":
        if len(function) == 1 or function[1] == "":
             ret_str = "Error: text not given"
        else:
            ret_str = translator.translate(function[1], src='en', dest='ta').text
            
    elif function[0] == "random-fact":    
        ret_str = requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()['text']
        
    elif function[0] == "text-to-binary":
        if len(function) == 1 or function[1] == "":
            ret_str = "Error: text not given"
        else:
            payload = {'text': function[1]}
            ret_str = requests.get('https://some-random-api.ml/binary', params=payload).json()['binary']
    
    return(ret_str)
    
#Emits the select * database query
def emit_all_from_database(channel, sid):
    all_messages = [
        db_message.message for db_message in
        db.session.query(chatDB.chatmessages).all()        
         ]
    print(all_messages)
    socketio.emit(channel, {
        'text': all_messages}, sid)
 
def add_to_db_and_emit(text):
    db.session.add(chatDB.chatmessages(text));
    db.session.commit();
    #emit_all_from_database('messages received')
        
@app.route('/')
def hello():
    return flask.render_template('index.html')


count = 0
@socketio.on('connect')
def on_connect():
    global count
    count += 1
    print('Someone connected!')
   

@socketio.on('disconnect')
def on_disconnect():
    global count
    count -= 1
    print ('Someone disconnected!')
    socketio.emit('connection', {
        'connection': count
    })
username = ""    
@socketio.on('new google user')
def on_new_google_user(data):
    sid = request.sid
    print("Got an event for new google user input with data:", data)
    global username
    username = data['name']
    socketio.emit('google user', {
        'username': username
    }, sid)
    socketio.emit('connection', {
        'connection': count
    })
    socketio.emit('chatArea', {
        'uname': username
    }, sid)
    print("connection status sent to user")
    #push_new_user_to_db(data['name'], models.AuthUserType.GOOGLE)
    emit_all_from_database('text received', sid)
    
@socketio.on('new message')
def on_new_data(data):
    sid = request.sid
    print("Got an event for data:", data)
    message = data['new message']
    global username
    if message != "":
        msg = username + ": " + message
        add_to_db_and_emit(msg)
        
    socketio.emit('text received', {
        'text': msg
    }) 
    if message[0:2] == '!!':
        bot_response = bot_response_api(message)
        add_to_db_and_emit("Bot: "+bot_response)
        socketio.emit('text received', {
            'text': "Bot: "+ bot_response
        }) 
 
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )