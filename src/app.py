import os
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from my_module import db_connection, db
from flask import Flask, request
from endpoints import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(api)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    emit('message', {'username': 'System', 'message': 'Connected to chat server'})

@socketio.on('message')
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    
    if username and message:
        # Store message in database
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_messages (username, message) VALUES (?, ?)",
            (username, message)
        )
        conn.commit()
        conn.close()

        # Broadcast message to all clients
        socketio.emit('message', {
            'username': username,
            'message': message
        }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)