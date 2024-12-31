import os
import jwt
from ..models.User import User
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from ..repository.ConnectionRepository import ConnectionRepository as ConnRepo
from ..models.Connection import Connection
from ..repository.RefreshRepository import RefreshRepository as RefreshRepo


class Jwt:
    @staticmethod
    def encode(payload):
        expiry_time = datetime.now() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
        ConnRepo.create_connection(payload.sub, expiry_time.isoformat())
        payload.update({"exp": expiry_time})
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    def decode(token):
        try:
            decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            jti = decoded.get("jti")
            id = int(decoded.get("sub"))
            if Connection.query.filter_by(id=id, key=jti).first() is not None:
                return decoded
            return {"error": "Connection not found"}
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid token"}
        finally:
            ConnRepo.delete_expired_connections()
        
    def generate_access_token(user : User):
        expiry_time = datetime.now() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 1)))
        jti = ConnRepo.create_connection(user.id, expiry_time.isoformat())
        return jwt.encode({"username": user.username, "sub": str(user.id), "jti": jti, "exp": expiry_time}, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    
    @staticmethod
    def get_sub_and_jti_from_expired_token(token) -> int:

        try:
            decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")], options={"verify_signature": False})
            return [int(decoded.get("sub")), decoded.get("jti")]
        except InvalidTokenError:
            return 0
       

    @staticmethod
    def generate_refresh_token(user : User):
        expiry_time = datetime.now() + timedelta(minutes=int(os.getenv("REFRESH_EXPIRATION_TIME", 60)))
        jti = RefreshRepo.create(user.id, user.uuid, expiry_time.isoformat())
        return jwt.encode({"sub": user.uuid, "jti": jti, "exp": expiry_time}, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    def decode_refresh_token(token):
        try:
            decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            jti = decoded.get("jti")
            uuid = decoded.get("sub")
            ref = RefreshRepo.get_refresh_by_jti(jti)
            if ref is not None and ref.uuid == uuid:
                return decoded
            RefreshRepo.delete_by_jti(jti)
            raise Exception("Refresh token ID not found")
        except ExpiredSignatureError:
            return {"error": "Refresh token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid refresh token"}