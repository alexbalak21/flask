from flask import Flask
from .db import db
app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db.init_app(app)




from .routes.home import home
from .routes.user import user







app.register_blueprint(home, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')