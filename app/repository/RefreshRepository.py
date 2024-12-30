from .. import db
from ..models.Refresh import Refresh
from datetime import datetime
import uuid

class RefreshRepository:
    
    def create(user_id :int, user_uuid: str, expires_at: str) -> str:
        """
        Create a new refresh token.

        Args:
            user_uuid (str): The UUID of the user.
            expires_at (str): The expiration time of the refresh token.

        Returns:
            str: jti for the token.
        """
        jti = str(uuid.uuid4())
        refresh = Refresh(id=user_id, uuid=user_uuid, jti=jti, expires_at=expires_at)
        db.session.add(refresh)
        db.session.commit()
        return jti


    def check_refresh_token(uuid: str, jti: str) -> bool:
        """
        Check if a refresh token exists by UUID and jti.

        Args:
            uuid (str): The UUID of the user.
            jti (str): The jti of the refresh token.

        Returns:
            bool: True if the refresh token exists, False otherwise.
        """
        refresh = Refresh.query.filter_by(uuid=uuid, jti=jti).first()
        return refresh is not None
    
    
    def get_id_by_jti(jti: str):
        """
        Get the ID of the refresh token by jti.

        Args:
            jti (str): The jti of the refresh token.

        Returns:
            dict: A dictionary representation of the refresh token if found, None otherwise.
        """
        refresh = Refresh.query.filter_by(jti=jti).first()
        refresh_time = datetime.fromisoformat(refresh.expires_at)
        if refresh_time < datetime.now():
            db.session.delete(refresh)
            db.session.commit()
            return None
        return refresh if refresh else None
    
    def delete_by_jti(jti: str) -> bool:
        """
        Delete a refresh token by jti.

        Args:
            jti (str): The jti of the refresh token.

        Returns:
            bool: True if the refresh token was deleted, False otherwise.
        """
        refresh = Refresh.query.filter_by(jti=jti).first()
        if refresh is None:
            return False
        db.session.delete(refresh)
        db.session.commit()
        return True
    
    def delete_expired_refresh_tokens():
        """
        Delete all expired refresh tokens.
        """
        for refresh in Refresh.query.all():
            if refresh.is_expired():
                db.session.delete(refresh)
        db.session.commit()
        
        