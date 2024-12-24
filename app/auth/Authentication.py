from flask import request, redirect, url_for
from ..auth.Jwt import Jwt

class Authentication:
    
    @staticmethod
    def required(f):
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            print("auth_header : ", auth_header)
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1] # Strip "Bearer " from the token
                print("token : ", token)
                print("claims : ", Jwt.decode(token))
                claims = Jwt.decode(token)
                if "error" in claims:
                    return redirect("/login-required")  # Redirect to 401 page if token is invalid
            else:
                return redirect("/login-required")  # Redirect to 401 page if no token is found
            return f(claims, *args, **kwargs)
        return decorated_function