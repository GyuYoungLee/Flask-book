import bcrypt  # pip install bcrypt

result = bcrypt.hashpw('password'.encode('UTF-8'), bcrypt.gensalt())  # 패스워드 생성
print(result, type(result))

ok = bcrypt.checkpw('password'.encode('UTF-8'), result)  # 패스워드 체크
print(ok)
