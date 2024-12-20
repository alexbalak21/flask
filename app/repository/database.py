from .. import db

def init_db():
    db.create_all()
    
def add_db():
    db.session.add(User(username="First User"))
    db.session.commit()
    