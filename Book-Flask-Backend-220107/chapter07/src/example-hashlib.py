import hashlib

result = hashlib.sha256("test password".encode('UTF-8')).hexdigest()
print(result)
