import bcrypt
key1 = "safaricom-api-key-1234567890abcdef"
key2 = "betika-api-key-0987654321fedcba"
print(bcrypt.hashpw(key1.encode(), bcrypt.gensalt()).decode())
print(bcrypt.hashpw(key2.encode(), bcrypt.gensalt()).decode())