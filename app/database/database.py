import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager

try:
    from app.config.database import DB_CONFIG
except ImportError:
    from app.config.database_example import DB_CONFIG

@contextmanager
def get_db():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_connection():
    return pymysql.connect(**DB_CONFIG)

