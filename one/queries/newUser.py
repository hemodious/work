from my_module import db_connection
from flask import jsonify,request
import sqlite3
class UserQuery:
    def __init__(self):
        pass
    def queryforstaff2():
        try:
             conn=db_connection()
             cursor=conn.cursor()
             issues=('crash issue','perfomance management issue','others')
             cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
             users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10] )
            for row in cursor.fetchall()
        ]
             cursor.close()
             conn.close()
             return users
        except:
            return jsonify({"error": "An error occurred"}), 500
    
    def queryforstaff1():
        try:
             conn=db_connection()
             cursor=conn.cursor()
             issues=('transaction issue','account management issue','security issue')
             cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
             users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10])
            for row in cursor.fetchall()
             ]
    
             return users
        except:
             return jsonify({"error": "An error occurred couldn't query database"}), 500
    
    def queryforall():
        try:
            conn=db_connection()
            cursor= conn.execute("SELECT * FROM user")#querying the table to get all user data
            users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9],status=row[10])
            for row in cursor.fetchall()
        ]#store  the data in a list of dictionaries
            if users is not None:# checking if the data is not empty
                return users
            
        except:
            return jsonify({"error": "An error occurred"}), 500
    
    def createNewUser(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id,update_status):
        try:
            conn=db_connection()
            sql="""INSERT INTO user (name,telephone,complaint,email,category,image,complaint_id,status)
            VALUES (?,?,?,?,?,?,?,?)"""
        # executing the query
            cursor=cursor.execute(sql,(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id,update_status))
            conn.commit()   
            conn.close()

        except:
            return jsonify({"error":"error adding new user"})
