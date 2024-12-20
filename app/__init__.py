from flask import Flask
from .routes.home import home
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db.init_app(app)

from .routes.user import user

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')