import jwt
from datetime import datetime, timedelta

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiQWxleCIsImp0aSI6ImU2NTE0Yjk2LTBhZWYtNDU1Yy05NDVlLTgyY2Y5MTM2YzQ3ZiIsImV4cCI6MTczNTU1MDk5Nn0.2ErI_ipMZqdp6I-CK7FAJij69_HppWfEi6-WWiwAZFQ"
try:
    decoded = jwt.decode(token, key="Super_Secret", algorithms=["HS256"], options={"verify_signature": False})
    print(decoded)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")