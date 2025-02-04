from jwt import encode, decode

def token_encode(payload):
    token = encode(payload=payload, key="secret", algorithm="HS256")
    return token

def token_decode(token):
    dec = decode(jwt=token, key="secret", algorithms=["HS256"])
    return dec

def test_enc_dec():
    encoded = encode(payload={"some": "payload"}, key="secret", algorithm="HS256")
    decoded = decode(encoded, "secret", algorithms=["HS256"])
    return decoded