db = {
    'user': 'root',
    'password': '1234qwer',
    'host': 'python-backend-test.crgxxeyyg5ot.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
