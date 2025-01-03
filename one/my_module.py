import sqlite3
from flask_sqlalchemy import SQLAlchemy


db= SQLAlchemy()
def db_connection():
    conn =None
    try:
        conn = sqlite3.connect('user.sqlite')
        conn.row_factory = sqlite3.Row 
    except sqlite3.error as e:
        print(e)
    return conn

