from flask import Blueprint, jsonify, request
from ..repository.UserRepository import UserRepository as UserRepo
from ..auth.Jwt import Jwt
from ..auth.Authentication import Authentication


user = Blueprint('user', __name__)

class UserRoutes:
    
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
        
        if not UserRepo.check_user(username):
            return jsonify({"msg": "User not found"}), 404
        current_user = UserRepo.check_login(username, password)
        if not current_user:
            return jsonify({"msg": "Wrong password"}), 401
        else:
            return jsonify({"access_token" : Jwt.encode({"sub" : current_user.id, "username": current_user.username}), "token_type" : "Bearer"}), 200
        
        
    @user.post("/logout")
    @Authentication.required
    def logout(claims):
        user_id = claims.get("sub")
        user = UserRepo.get_one(user_id)
        if user is None:
            return jsonify({"msg": "Forbidden"}), 401
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]  # Strip "Bearer " from the token
            Jwt.blacklist_token(token)
            return jsonify({"msg": "Successfully logged out"}), 200
        return jsonify({"msg": "Token not found"}), 400

    
    @user.get("/profile")
    @Authentication.required
    def get_profile(claims):
        user_id = claims.get("sub")
        user = UserRepo.get_one(user_id)
        if user is None:
            return jsonify({"msg": "user not found"}), 404
        return jsonify(user)
    

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


    @user.delete("/<int:user_id>")
    def delete(user_id):
        user = UserRepo.get_one(user_id)
        if user is None:
            return jsonify({"msg": "user not found"}), 404
        UserRepo.delete_user(user_id)
        return jsonify({"msg": "user successfully deleted"}), 200
    