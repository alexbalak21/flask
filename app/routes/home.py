from flask import Blueprint

home = Blueprint('home', __name__)

@home.get('/')
def home_page():
    return "<h1>Home</h1>"