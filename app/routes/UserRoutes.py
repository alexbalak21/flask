from flask import Blueprint, jsonify, request
from ..repository.UserRepository import UserRepository as UserRepo
from ..models.User import User


user = Blueprint('user', __name__)

class UserRoutes:
    
    def get_authorization_header(f):
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                print(f"Authorization : {auth_header}")
            else:
                print("No Authorization Header found")
            return f(*args, **kwargs)
        return decorated_function


    @user.get("/init")
    def home_page():
        UserRepo.init_db()
        return "Database Init Done."

    @user.get('/')
    @get_authorization_header
    def init():
        return "User Home"

    @user.post("/signin")
    def signin():
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return jsonify({"msg": "Bad username or password"}), 401
        try:
            new_user = UserRepo.create_user(username, password)  # Fixed function call
            return jsonify(new_user), 201
        except ValueError as e:
            if str(e) == "Username already exists. Please choose a different one.":
                # Conflict status code for existing resource
                return jsonify({"msg": str(e)}), 409
            return jsonify({"msg": "An error occurred. Please try again."}), 500
        except Exception as e:
            return jsonify({"msg": "Failed to add user to db."}), 500
        
    @user.post("/login")
    def login():
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return jsonify({"msg": "Bad username or password"}), 401
        
        
    @user.get("/all")
    def get_all_users():
        return jsonify(UserRepo.get_all())

    @user.get('/<int:id>')
    def find_by_id(id):
        user = UserRepo.get_one(id)
        if user is None:
            return jsonify({"msg": "user not found"}), 404
        return jsonify(user)

    @user.put("/<int:user_id>")
    def update(user_id):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username and not password:
            return jsonify({"msg": "Nothing to update"}), 401
        updated_user = UserRepo.update_user(user_id, username, password)
        if updated_user is None:
            return jsonify({"msg": "user not found"}), 404
        else:
            return jsonify(updated_user), 200

    @user.delete("<int:user_id>")
    def delete_user():
        return None