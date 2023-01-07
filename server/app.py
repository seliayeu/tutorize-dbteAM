import hashlib
import os

from db_interface import create_user, get_courses, login_user, get_user_chatrooms, get_user_chat_history, send_message
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from models import Course, db, setup
from flask_socketio import SocketIO
import time

load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), 'database.db')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60*60*24
db.init_app(app)
jwt = JWTManager(app)
socketio = SocketIO(app)

def gen_login_token(username):
    create_access_token(identity=username)


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    create_user(username, password)

    return jsonify(success=True), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    token = login_user(username, password)

    if token:
        return jsonify(token=token), 200
    else:
        return jsonify(message='Access Denied'), 401


@app.route('/courses', methods=["GET"])
def get():
    return jsonify(courses=get_courses()), 200


@app.route('/chatrooms', methods=["GET"])
@jwt_required()
def get_chatrooms():
    username = get_jwt_identity()
    chatrooms = get_user_chatrooms(username)
    return jsonify(chatrooms), 200


@app.route('/chat_history', methods=["POST"])
@jwt_required()
def get_chat_history():
    username = get_jwt_identity()
    chatroom_id = request.json['chatroom_id']
    message_history = get_user_chat_history(username, chatroom_id)
    return jsonify(message_history), 200


@app.route('/message', methods=["POST"])
@jwt_required()
def send_message_handler():
    from_user = get_jwt_identity()
    to_user = request.json['recipient']
    content = request.json['content']
    timestamp = int(time.time())
    send_message(from_user, to_user, content, timestamp)
    return jsonify(success=True), 200


@app.route('/live', methods=["POST"])
@jwt_required()
def live_ping():
    subjects = request.json['subjects']
    location_lat = request.json['location_lat']
    location_long = request.json['location_long']


if __name__ == '__main__':
    with app.app_context():
        setup()
    app.run(debug=True)