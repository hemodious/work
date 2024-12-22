import sqlite3
def init_db():
    conn = sqlite3.connect('Staff.db')
    cursor = conn.cursor()
    staff=[
        ('Emmanuel','affoh.emmanuel.ea@gmail.com','password'),
        ('Michael','michaelopoku790@gmail.com','password')
    ]
    cursor.executemany("""
            INSERT INTO Staff (name ,email ,password)
            VALUES (?,?,?)
            
    """,staff)
    
    conn.commit()
    conn.close()

init_db()