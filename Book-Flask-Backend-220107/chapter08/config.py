db = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

test_config = {
    'DB_URL': DB_URL
}
