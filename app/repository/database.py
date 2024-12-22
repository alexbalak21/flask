from .. import db
from ..models.User import User
from sqlalchemy.exc import IntegrityError


def init_db():
    db.drop_all()
    db.create_all()


def add_db():
    db.session.add(User(username="First User", password="pass"))
    db.session.commit()


def create_user(username, password):
    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError(
            "Username already exists. Please choose a different one.")

    # Proceed with creating the new user
    new_user = User(username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        print("USER CREATED")
        return new_user.as_dict()
    except IntegrityError:
        print("ERROR CREATING USER")
        db.session.rollback()
        raise ValueError("There was an error while creating the user.")


def get_one(id: int):
    user = User.query.filter_by(id=id).first()
    return None if user is None else user.as_dict()


def update_user(id: int):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return None


def get_all():
    users = [user.as_dict() for user in User.query.all()]
    return users
