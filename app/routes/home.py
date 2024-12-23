from flask import Blueprint, jsonify
from ..repository.init_db import init_db
home = Blueprint('home', __name__)

@home.get('/')
def home_page():
    return "<h1>Home</h1>"


@home.get("/init")
def init():
    init_db()
    return jsonify({"msg": "Database Init Done."})