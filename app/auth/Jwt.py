import os
import jwt
import uuid
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from ..models.Blacklist import Blacklist
from ..models.Connection import Connection
from ..db_conn import db


class Jwt:
    @staticmethod
    def encode(payload):
        expiry_time = datetime.utcnow() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
        payload.update({"exp": expiry_time, "jti": str(uuid.uuid4())})
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    def decode(token):
        try:
            decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            jti = decoded.get("jti")
            id = decoded.get("sub")
            if Connection.query.filter_by(id=id, key=jti).first() is not None:
                return decoded
            return {"error": "Invalid token"}
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid token"}