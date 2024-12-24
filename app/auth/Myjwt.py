import base64
import json
import hmac
import hashlib
import time

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64_url_decode(data):
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)



def create_jwt(payload, secret):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    header_encoded = base64_url_encode(json.dumps(header).encode('utf-8'))
    payload_encoded = base64_url_encode(json.dumps(payload).encode('utf-8'))
    signature = hmac.new(secret.encode('utf-8'), f'{header_encoded}.{payload_encoded}'.encode('utf-8'), hashlib.sha256).digest()
    signature_encoded = base64_url_encode(signature)
    return f'{header_encoded}.{payload_encoded}.{signature_encoded}'


# Example usage
secret_key = 'your_secret_key'
payload = {
    'user_id': 123,
    'exp': int(time.time()) + 3600  # Token expires in 1 hour
}
token = create_jwt(payload, secret_key)
print(f"Generated JWT: {token}")




def verify_jwt(token, secret):
    header_encoded, payload_encoded, signature_encoded = token.split('.')
    signature = base64_url_decode(signature_encoded.encode('utf-8'))
    valid_signature = hmac.new(secret.encode('utf-8'), f'{header_encoded}.{payload_encoded}'.encode('utf-8'), hashlib.sha256).digest()
    if not hmac.compare_digest(signature, valid_signature):
        raise ValueError("Invalid token signature")
    payload = json.loads(base64_url_decode(payload_encoded.encode('utf-8')))
    if payload['exp'] < time.time():
        raise ValueError("Token has expired")
    return payload

# Example usage
try:
    decoded_payload = verify_jwt(token, secret_key)
    print(f"Decoded payload: {decoded_payload}")
except ValueError as e:
    print(e)