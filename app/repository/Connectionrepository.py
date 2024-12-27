from .. import db
from ..models.Connection import Connection


class ConnectionRepository:
    
    def create_connection(id: int, key: str) -> dict:
        new_connection = Connection(id=id, key=key)
        db.session.add(new_connection)
        db.session.commit()
        return new_connection.as_dict()

    
    def get_by_key(key: str):
        connection = Connection.query.filter_by(key=key).first()
        return None if connection is None else connection.as_dict()
    
    def update_connection(old_key: str, new_key: str):
        connection = Connection.query.filter_by(key=old_key).first()
        if connection is None:
            return None
        connection.key = new_key
        db.session.commit()
        return connection.as_dict()
      
    
    def delete_connection_by_key(key: str):
        connection = Connection.query.filter_by(key=key).first()
        if connection is None:
            raise ValueError("Connection not found.")
        db.session.delete(connection)
        db.session.commit()
        return connection.as_dict()
