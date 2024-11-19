
import os
from flask_socketio import  SocketIO, send
from flask_cors import  CORS
#from my_module import chat_connection
from flask import Flask 
from endpoints import api
app = Flask(__name__)

CORS(app)  # Allow your client origin

app.register_blueprint(api)
socketio= SocketIO(app)

@socketio.on('connect')
def handle_connect():
 send('Client connected', broadcast=True)
#message handler
@socketio.on('message')
def handlemessages(data):
    username= data['username']
    message= data['message']

    conn= ''
    cursor= conn.cursor()
    cursor.execute("INSERT INTO chat_messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()

    socketio.send({'username' : username, 'message' : message})
    

if __name__ == '__main__':
    #
   socketio.run(app,debug=True)