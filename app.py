from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

