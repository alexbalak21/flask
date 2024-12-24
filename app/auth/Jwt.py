import os
import jwt
import uuid
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import redis

# Initialize Redis client
redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), db=0)

class Jwt:
    @staticmethod
    def encode(payload):
        expiry_time = datetime.now() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
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
        decoded = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")], options={"verify_exp": False})
        return decoded.get("jti")
    
    @staticmethod
    def blacklist_token(token):
        jti = Jwt.get_jti(token)
        redis_client.set(jti, "blacklisted", ex=int(os.getenv("EXPIRATION_TIME", 15)) * 60)
        
    @staticmethod
    def is_blacklisted(jti):
        return redis_client.get(jti) is not None