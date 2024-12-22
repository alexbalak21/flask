from .. import db
from ..models.User import User


def init_db():
    db.drop_all()
    db.create_all()


def add_db():
    db.session.add(User(username="First User"))
    db.session.commit()


def add_user(username, password):
    db.session.add(User(username=username, password=password))
    db.session.commit()
    return
