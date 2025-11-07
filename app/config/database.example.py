from pymysql.cursors import DictCursor

DB_CONFIG = {
    "host": "your_host",
    "user": "your_user",
    "password": "your_password",
    "database": "your_database",
    "cursorclass": DictCursor
}