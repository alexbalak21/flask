import os
import jwt
import uuid
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from ..models.Blacklist import Blacklist
from ..db_conn import db


class Jwt:
    @staticmethod
    def encode(payload):
        expiry_time = datetime.utcnow() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
        payload.update({"exp": expiry_time, "jti": str(uuid.uuid4())})
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    @staticmethod
    def decode(token):
        jti = Jwt.get_jti(token)
        if Jwt.is_blacklisted(jti):
            return {"error": "Token has been blacklisted"}
        try:
            return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid token"}

    @staticmethod
    def get_jti(token):
        decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[
                             os.getenv("ALGORITHM")], options={"verify_exp": False})
        return decoded.get("jti")

    @staticmethod
    def blacklist_token(token):
        jti = Jwt.get_jti(token)
        blacklisted_token = Blacklist(jti=jti)
        db.session.add(blacklisted_token)
        db.session.commit()

    @staticmethod
    def is_blacklisted(jti):
        return db.session.query(Blacklist).filter_by(jti=jti).first() is not None
