import sqlite3

conn = sqlite3.connect("User.db")


cursor =conn.cursor()
sql_query=""" CREATE TABLE user (
    id integer PRIMARY KEY,
    name text NOT NULL,
    telephone integer NOT NULL,
    complaint text NOT NULL,
    email  text NOT NULL,
    category text NOT NULL,
    complaint_id text NOT NULL
)"""
cursor.execute(sql_query)
conn.commit()
conn.close()