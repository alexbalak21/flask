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

secret_key = 'my_secret_key'
expires_in = 3600  # 1 hour


#CREATE JWT
def create_jwt(payload):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    header_encoded = base64_url_encode(json.dumps(header).encode('utf-8'))
    
    # Add exp claim to payload
    payload['exp'] = int(time.time()) + expires_in
    payload_encoded = base64_url_encode(json.dumps(payload).encode('utf-8'))
    
    signature = hmac.new(secret_key.encode('utf-8'), f'{header_encoded}.{payload_encoded}'.encode('utf-8'), hashlib.sha256).digest()
    signature_encoded = base64_url_encode(signature)
    return f'{header_encoded}.{payload_encoded}.{signature_encoded}'


#VERIFY JWT
def verify_jwt(token):
    header_encoded, payload_encoded, signature_encoded = token.split('.')
    signature = base64_url_decode(signature_encoded.encode('utf-8'))
    valid_signature = hmac.new(secret_key.encode('utf-8'), f'{header_encoded}.{payload_encoded}'.encode('utf-8'), hashlib.sha256).digest()
    if not hmac.compare_digest(signature, valid_signature):
        return False
    
    # Decode payload and check exp claim
    payload = json.loads(base64_url_decode(payload_encoded.encode('utf-8')))
    if 'exp' in payload and payload['exp'] < time.time():
        return False
    
    return True
