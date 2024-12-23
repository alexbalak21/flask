from .. import db
from ..models.User import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class UserRepository:

    def init_db():
        db.drop_all()
        db.create_all()

    def create_user(username: str, password: str) -> dict:
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError(
                "Username already exists. Please choose a different one.")

        # Proceed with creating the new user
        new_user = User(username=username,
                        password=generate_password_hash(password))
        try:
            db.session.add(new_user)
            db.session.commit()
            print("USER CREATED")
        except IntegrityError:
            print("ERROR CREATING USER")
            db.session.rollback()
            raise ValueError("There was an error while creating the user.")

        return new_user.as_dict()

    def get_one(id: int):
        user = User.query.filter_by(id=id).first()
        return None if user is None else user.as_dict()

    def update_user(id: int, new_username=None, new_password=None):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return None
        if new_username is not None:
            user.username = new_username
        if new_password is not None:
            # Ensure you hash the password before storing it
            user.password = generate_password_hash(new_password)

        db.session.commit()
        return user.as_dict()

    def get_all():
        users = [user.as_dict() for user in User.query.all()]
        return users

    def delete_user(id: int):
        user = User.query.filter_by(id=id).first()
        if user is None:
            raise ValueError("User not found.")
        try:
            db.session.delete(user)
            db.session.commit()
            return {"msg": "User successfully deleted."}
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(
                "There was an error while deleting the user: " + str(e))
