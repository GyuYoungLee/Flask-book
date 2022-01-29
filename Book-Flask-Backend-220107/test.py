import bcrypt  # pip install bcrypt
import jwt
from datetime import datetime, timedelta

result = bcrypt.hashpw('gy'.encode('UTF-8'), bcrypt.gensalt())  # 패스워드 생성
print(result)
# print(result.encode('UTF-8'))

ok = bcrypt.checkpw('password'.encode('UTF-8'), result)  # 패스워드 체크
print(ok)

# payload = {
#     'user_id': 'gy',
#     'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
# }
#
# token = jwt.encode(payload, 'secret', 'HS256')  # 토큰 생성
# print(token)
#
# data = jwt.decode(token, 'secret', 'HS256')  # 토큰 복호화
# print(data)
