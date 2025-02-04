import secrets
import string

class Utils:
    
    @staticmethod
    def generate_unique_string(length=16):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    