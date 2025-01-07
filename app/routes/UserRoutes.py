from flask import Blueprint, jsonify, request
from ..repository.UserRepository import UserRepository as UserRepo
from ..auth.Jwt import Jwt
from ..auth.Authentication import Authentication
from ..repository.ConnectionRepository import ConnectionRepository as ConnRepo
from ..repository.RefreshRepository import RefreshRepository as RefreshRepo


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
        if not UserRepo.user_exists_by_username(username):
            return jsonify({"msg": "User not found"}), 404
        current_user = UserRepo.check_login(username, password)
        if not current_user:
            return jsonify({"msg": "Wrong password"}), 401
        else:
            access_token = {"access_token" : Jwt.generate_access_token(current_user), "token_type" : "Bearer"}
            refresh_token = {"refresh_token" : Jwt.generate_refresh_token(current_user), "refresh_token_type" : "X-Refresh-Token"}
            return jsonify(access_token, refresh_token), 200
        
        
    @user.post("/logout")
    @Authentication.required
    def logout(claims):
        id = claims.get("sub")
        user = UserRepo.get_by_id(id)
        if user is None:
            return jsonify({"msg": "Forbidden"}), 401
        if ConnRepo.delete_connection_by_key(claims.get("jti")) :
            return jsonify({"msg": "Successfully logged out"}), 200
        return jsonify({"msg": "Login information not found"}), 401
    
    @user.post("/refresh")
    def refresh():
        refresh_token = request.headers.get("X-Refresh-Token", None)
        auth_token = request.headers.get("Authorization", None)
        if not refresh_token or not auth_token:
            return jsonify({"msg": "No refresh token or auth token provided"}), 401
        try:    
            refresh_data = Jwt.decode_refresh_token(refresh_token)
            sub, rti = refresh_data.get("sub"), refresh_data.get("jti")
            [user_id, jti] = Jwt.get_sub_and_jti_from_expired_token(auth_token.split(" ")[1])

            user = UserRepo.get_user_by_id_and_uuid(user_id, sub)
            refresh_id = RefreshRepo.get_refresh_by_jti(rti).id
            if user is None:
                return jsonify({"msg": "User not found"}), 404
            if refresh_id == 0 or user_id != refresh_id:
                return jsonify({"msg": "Invalid refresh token"}), 401
            #DELETING OLD AUTH AND REFRESH TOKEN
            RefreshRepo.delete_by_jti(rti)
            ConnRepo.delete_by_jti(jti)
            res = {"access_token" : Jwt.generate_access_token(user), "token_type" : "Bearer", "refresh_token" : Jwt.generate_refresh_token(user), "refresh_token_type" : "X-Refresh-Token"}
            return jsonify(res), 200
        except Exception as e:
            return jsonify({"msg": e.__str__()}), 401

    
    @user.get("/profile")
    @Authentication.required
    def get_profile(claims):
        user_id = claims.get("sub")
        user = UserRepo.get_by_id(user_id)
        if user is None:
            return jsonify({"msg": "user not found"}), 404
        return jsonify(user)
    

    @user.get("/all")
    def get_all_users():
        return jsonify(UserRepo.get_all())


    @user.get('/<int:id>')
    def find_by_id(id):
        user = UserRepo.get_by_id(id)
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
        user = UserRepo.get_by_id(user_id)
        if user is None:
            return jsonify({"msg": "user not found"}), 404
        UserRepo.delete_user(user_id)
        return jsonify({"msg": "user successfully deleted"}), 200
    