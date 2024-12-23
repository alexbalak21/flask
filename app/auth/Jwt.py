import os
import jwt

class Jwt:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.expiry_time= os.getenv("EXPIRATION_TIME")
        self.issuer
        self.audience
    
    @staticmethod
    def encode(payload):
        return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    
    @staticmethod
    def decode(token):
        return jwt.decode(token, key= os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])