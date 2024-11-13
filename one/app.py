
from flask_socketio import  SocketIO, send
from flask_cors import  CORS

from flask import Flask 
from endpoints import api
app = Flask(__name__)
CORS(app)
app.register_blueprint(api)
socketio= SocketIO(app)

#message handler
@socketio.on('message')
def handlemessages(msg):
    print('Message: '+ str(msg))
    send(msg,broadcast=True)

if __name__ == '__main__':
    #
    socketio.run(app,debug=True)