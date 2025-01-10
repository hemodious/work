from my_module import db_connection,staff_connection
from flask import jsonify,request
from constants.vars import *
import sqlite3
class UserQuery:
    def __init__(self):
        pass
    
    
            
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
            cursor=conn.execute(sql,(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id,update_status))
            conn.commit()   
            conn.close()

        except:
            return jsonify({"error":"error adding new user"})
   