from .. import db
from ..models.Connection import Connection
import uuid

class ConnectionRepository:
    
    @staticmethod
    def create_connection(id: int,expires_at: str) -> str:
        """
        Create a new connection.

        Args:
            id (int): The ID of the connection.
            expires_at (str): The expiration time of the connection.

        Returns:
            str: jti for the token.
        """
        key = str(uuid.uuid4())
        connection = Connection(id=id, key=key, expires_at=expires_at)
        db.session.add(connection)
        db.session.commit()
        return key
    
    @staticmethod
    def check_connection_exists(key: str) -> bool:
        """
        Check if a connection exists by key.

        Args:
            key (str): The key of the connection.

        Returns:
            bool: True if the connection exists, False otherwise.
        """
        connection = Connection.query.filter_by(key=key).first()
        return connection is not None
    
    @staticmethod
    def get_by_key(key: str):
        """
        Get a connection by key.

        Args:
            key (str): The key of the connection.

        Returns:
            dict: A dictionary representation of the connection if found, None otherwise.
        """
        connection = Connection.query.filter_by(key=key).first()
        return None if connection is None else connection.as_dict()
    
    @staticmethod
    def update_connection(old_key: str, new_key: str):
        """
        Update a connection's key.

        Args:
            old_key (str): The old key of the connection.
            new_key (str): The new key of the connection.

        Returns:
            dict: A dictionary representation of the updated connection if found, None otherwise.
        """
        connection = Connection.query.filter_by(key=old_key).first()
        if connection is None:
            return None
        connection.key = new_key
        db.session.commit()
        return connection.as_dict()
    
    @staticmethod
    def delete_expired_connections():
        """
        Delete all expired connections.

        Returns:
            int: The number of connections deleted.
        """
        connections = Connection.query.all()
        count = 0
        for connection in connections:
            if connection.is_expired():
                db.session.delete(connection)
                count += 1
        db.session.commit()
        return count