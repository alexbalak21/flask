from flask import Blueprint, jsonify, request
from ..repository.database import init_db, add_db, create_user, get_all
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
    if not username or not password:
        return jsonify({"msg": "Bad username or password"}), 401
    try:
        new_user = create_user(username, password)  # Fixed function call
        return jsonify(new_user), 201
    except ValueError as e:
        if str(e) == "Username already exists. Please choose a different one.":
            # Conflict status code for existing resource
            return jsonify({"msg": str(e)}), 409
        return jsonify({"msg": "An error occurred. Please try again."}), 500
    except Exception as e:
        return jsonify({"msg": "Failed to add user to db."}), 500


@user.get("/all")
def get_all_users():
    return jsonify(get_all())
