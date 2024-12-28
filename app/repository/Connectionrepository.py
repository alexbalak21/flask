from .. import db
from ..models.Connection import Connection


class ConnectionRepository:
    
    #CREATE CONNECTION RETURN CONNECTION TRUE OR FALSE
    def create_connection(id: int, key: str) -> bool:
        connection = Connection(id=id, key=key)
        db.session.add(connection)
        db.session.commit()
        return True

    
    #CHECK IF CONNECTION EXISTS BY KEY
    def check_connection_exists(key: str) -> bool:
        connection = Connection.query.filter_by(key=key).first()
        return connection is not None
    
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
    
    
    def delete_connection_by_id(id: int):
        connection = Connection.query.filter_by(id=id).first()
        if connection is None:
            return False
        db.session.delete(connection)
        db.session.commit()
        return True
