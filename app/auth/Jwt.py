import os
import jwt

class Jwt:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.expiry_time
        self.issuer
        self.audience
    
    def encode(self, payload):
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode(self, token):
        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)