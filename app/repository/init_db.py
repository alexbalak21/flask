from app import app
from ..db_conn import db
from ..models.User import User
from ..models.Article import Article

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        return True