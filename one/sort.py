import sqlite3
from datetime import datetime

# Connect to the database (or create it)
conn = sqlite3.connect('chat.db')
c = conn.cursor()

# Create a table for chat messages
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY, user_id TEXT, message TEXT, timestamp TEXT)''')
