from flask import Blueprint
from ..repository.database import init_db, add_db


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