from flask import Blueprint
from repository.database import init_db, add_db

home = Blueprint('home', __name__)

@home.get('/')
def homepage():
    return "Home"


@home.get("/init")
def init():
    

