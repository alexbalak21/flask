import secrets
import string

def generate_unique_string(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Generate a unique string
unique_string = generate_unique_string()
print(f"Generated unique string: {unique_string}")