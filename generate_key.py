import secrets

# Generate a secure secret key
secret_key = secrets.token_hex(32)
print("Your secure SECRET_KEY:")
print(secret_key) 