from .. import db
from ..models.User import User


def init_db():
    db.drop_all()
    db.create_all()


def add_db():
    db.session.add(User(username="First User", password="pass"))
    db.session.commit()


def add_user(username, password):
    db.session.add(User(username=username, password=password))
    try:
        db.session.commit()
    except:
        return False
    return True


def get_all():
    users = User.query.all().__str__()
    return users
