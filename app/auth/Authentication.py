from flask import request, redirect, url_for
from ..auth.Jwt import Jwt

class Authentication:
    
    @staticmethod
    def required(f):
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]  # Strip "Bearer " from the token
                claims = Jwt().decode(token)
                if "error" in claims:
                    ##REDIRECT TO LOGIN-REQUIRED PAGE
                    return redirect("/login-required?error=Invalid Token")  # Redirect to login page if token is invalid
            else:
                return redirect("/login-required?error=No Authorization found in header")  # Redirect to login page if no auth header
            ##RETURN FUNCTION
            return f(claims, *args, **kwargs)
        decorated_function.__name__ = f.__name__  # Ensure the function name is unique
        return decorated_function