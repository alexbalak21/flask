from flask import Blueprint
from ..repository.database import init_db, add_db

user = Blueprint('user', __name__)

@user.get('/')
def home():
    return "User Home"

@user.get("/init")
def home_page():
    init_db()
    return "Database Init Done."