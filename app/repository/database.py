from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .. import app
from .. import db
from ..models.User import User

def init_db():
    db.create_all()
    
def add_db():
    db.session.add(User(username="First User"))
    db.session.commit()
    