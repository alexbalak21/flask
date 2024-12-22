from flask import Blueprint, jsonify, request
from ..repository.database import init_db, add_db, add_user
from ..models.User import User


user = Blueprint('user', __name__)


@user.get('/create')
def home():
    add_db()
    return "Create user"


@user.get("/init")
def home_page():
    init_db()
    return "Database Init Done."


@user.get('/')
def init():
    return "User Home"


@user.post("/signin")
def signin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username == None or password == None:
        return jsonify({"msg": "Bad username or password"}), 401
    try:
        add_user(username, password)
        return jsonify({"msg": f'{username} added to the database.'}), 201
    except:
        return jsonify({"failed to add user to db."}), 501
