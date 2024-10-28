import sqlite3

conn = sqlite3.connect("user.sqlite")


cursor =conn.cursor()
sql_query=""" CREATE TABLE user (
    id integer PRIMARY KEY,
    name text NOT NULL,
    telephone integer NOT NULL,
    complaint text NOT NULL,
    email  text NOT NULL,
    category text NOT NULL,
)"""
cursor.execute("""ALTER TABLE user ADD COLUMN complaint_id""")
conn.commit()
conn.close()