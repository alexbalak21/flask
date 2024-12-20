from flask import Flask
from .routes.home import home

app = Flask(__name__)

from .routes.user import user



app.register_blueprint(home, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')