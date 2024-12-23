from flask import request, redirect
from ..auth.Jwt import Jwt

class Authentication:
    
    def authentication_required(f):
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                claims = Jwt.decode(auth_header.split(" ")[1]) # Strip bearer from token
            else:
                return redirect("/login-required")
            return f(claims ,*args, **kwargs)
        return decorated_function