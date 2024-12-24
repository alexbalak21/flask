import os
import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class Jwt:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.expiry_time = int(os.getenv("EXPIRATION_TIME", 15))  # Default to 15 minutes if not set
        self.issuer = os.getenv("ISSUER")
        self.audience = os.getenv("AUDIENCE")
    
    @staticmethod
    def encode(payload):
        expiry_time = datetime.now() + timedelta(minutes=int(os.getenv("EXPIRATION_TIME", 15)))
        payload.update({"exp": expiry_time})
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    
    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        except ExpiredSignatureError:  
            return {"error": "Token has expired"}
        except InvalidTokenError:
            return {"error": "Invalid token"}