from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models.user import User
from models.article import Article

@app.route('/')
def index():
    return "Welcome to the Blog Application!"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)