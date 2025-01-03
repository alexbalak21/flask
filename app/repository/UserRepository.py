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
        except IntegrityError:
            db.session.rollback()
            raise ValueError("There was an error while creating the user.")

        return new_user.as_dict()
    
    def get_all() -> list:
        users = [user.as_dict() for user in User.query.all()]
        return users

    def get_by_id(id: int):
        user = User.query.filter_by(id=id).first()
        return user.as_dict() if user else None
    
    def get_user_by_id_and_uuid(id : int, uuid: str) -> User:
        user = User.query.filter_by(id=id, uuid=uuid).first()
        return user if user else None


    def update_user(id: int, new_username=None, new_password=None):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return None
        if new_username is not None:
            user.username = new_username
        if new_password is not None:
            user.password = generate_password_hash(new_password)
            
        db.session.commit()
        return user.as_dict()


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
            
    def user_exists_by_username(username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None
    
    def user_exists_by_id(id : int) -> bool:
        return User.query.filter_by(id=id).first() is not None
            
    def check_login(username: str, password: str):
        user = User.query.filter_by(username=username).first()
        return user if user and check_password_hash(user.password, password) else None

        
