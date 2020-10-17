import os
import flask
import flask_socketio
from os.path import join, dirname
from dotenv import load_dotenv
import flask_sqlalchemy
import flask_socketio
import chatDB
import random
from flask import request
import requests
import json
from googletrans import Translator
translator = Translator()
 
#Initializing things
app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']
    
#Initializing database
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()
 
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
        
def randomAnimal(used_animal_names):
    list_animals = ["duck", "orangutan", "cow", "chicken","horse","fish","zebra","goat","lion","peacock"]
    random_animal = list_animals[random.randint(0,len(list_animals)-1)]
    while random_animal in used_animal_names:
        random_animal = list_animals[random.randint(0,len(list_animals)-1)]
    return random_animal
    
#Emits the select * database query
def emit_all_from_database(channel):
    all_messages = [
        db_message.message for db_message in
        db.session.query(chatDB.chat_messages).all()        
         ]
    socketio.emit(channel, {
        'text': all_messages})
 
def add_to_db_and_emit(text):
    db.session.add(chatDB.chat_messages(text));
    db.session.commit();
    emit_all_from_database('messages received')
        
@app.route('/')
def hello():
    return flask.render_template('index.html')

username_sid = {}
used_animal_names = set()
count = 0
@socketio.on('connect')
def on_connect():
    global count
    count += 1
    print('Someone connected!')
    sid = request.sid
    socketio.emit('connection', {
        'connection': count
    })
    print("connection status sent to user")
    
    
    #Creates a random username
    random_animal = randomAnimal(used_animal_names)
    used_animal_names.add(random_animal)
    user_name = "anonymous_" + random_animal
    socketio.emit('user name', {
        'username': user_name
    }, sid)
    #Assigns sid to username
    username_sid[sid] = user_name
   
   
@socketio.on('disconnect')
def on_disconnect():
    global count
    count -= 1
    print ('Someone disconnected!')
    socketio.emit('connection', {
        'connection': count
    })
    
@socketio.on('new google user')
def on_new_google_user(data):
    sid = request.sid
    print("Got an event for new google user input with data:", data)
    socketio.emit('google user', {
        'connection': "google"
    }, sid)
    #push_new_user_to_db(data['name'], models.AuthUserType.GOOGLE)
    emit_all_from_database('text received')
    
@socketio.on('new message')
def on_new_number(data):
    sid = request.sid
    print("Got an event for new number with data:", data)
    message = data['new message']
    if message != "":
        msg = username_sid[sid] + ": " + message
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