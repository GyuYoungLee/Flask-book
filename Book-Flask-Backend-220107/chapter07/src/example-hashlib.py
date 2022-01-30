import hashlib

result = hashlib.sha256("tests password".encode('UTF-8')).hexdigest()
print(result)
