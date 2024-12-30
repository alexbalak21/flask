from flask import Blueprint, jsonify, request
from ..repository.init_db import init_db
home = Blueprint('home', __name__)

@home.get('/')
def home_page():
    return jsonify({"msg": "Home Page"})


@home.get("/init")
def init():
    init_db()
    return jsonify({"msg": "Database Init Done."})


@home.get("/login-required")
##GET THE MESSAGE IN THE URL
def login_required():
    error = request.args.get("error")
    res = {"msg": "Login Required"}
    if error:
        res["error"] = error
    return jsonify(res), 401