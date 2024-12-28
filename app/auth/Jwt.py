import os
import jwt
import uuid
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from ..repository.ConnectionRepository import ConnectionRepository as ConnRepo
from ..models.Connection import Connection


class Jwt:
    @staticmethod
    def encode(payload):
        expiry_time = datetime.utcnow() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
        payload.update({"exp": expiry_time})
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    def decode(token):
        try:
            decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            jti = decoded.get("jti")
            id = decoded.get("sub")
            if Connection.query.filter_by(id=id, key=jti).first() is not None:
                return decoded
            return {"error": "Connection not found"}
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid token"}