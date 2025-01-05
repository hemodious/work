from my_module import db_connection
from flask import jsonify,request
from constants.vars import *
import sqlite3
class UserQuery:
    def __init__(self):
        pass
    def queryforstaff2():
        #function to query all complaints belonging to staff2 depending on the category
   
        page =request.args.get('page',1,type=int)
        per_page= request.args.get('per_page',10,type=int)
        offset = (page - 1) * per_page
        conn=db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?) LIMIT ? OFFSET ?',(*issues,per_page,offset))
        users=[
                dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10] )
                for row in cursor.fetchall()
            ]
        
        cursor.execute('SELECT COUNT(*) FROM user WHERE category IN (?,?,?)',issues)
        total = cursor.fetchone()[0]
        conn.close()
        total_pages=(total // per_page) + (1 if total % per_page > 0 else 0)

        response ={
            'users': users,
            'pagination': {
                'total': total,
                'page': page,
                'pages': total_pages,
                'per_page': per_page,
                'next_page': f"/staff2?page={page + 1}&per_page={per_page}" if page < total_pages else None,
                'prev_page': f"/staff2?page={page - 1}&per_page={per_page}" if page > 1 else None,
        }
        }
        return (response)


    
    def queryforstaff1():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int) 
            offset = (page - 1) * per_page 
            try:
                conn=db_connection()
            except sqlite3.Error as e:
                 return jsonify({"message": "Database connection failed"}), 500
            cursor=conn.cursor()
            try:
                cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?) LIMIT ? OFFSET ?',(*issues,per_page,offset))
                users=[
                    dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10])
                    for row in cursor.fetchall()
                ]
                if users is None:
                     return jsonify({"message": "No users found"}), 404
            except sqlite3.Error as e:
                 return jsonify({"message": "Database query failed"}), 500
            print (users)
            cursor.execute('''
                SELECT COUNT(*) FROM user 
                WHERE category IN (?, ?, ?)
            ''', issues)
            total = cursor.fetchone()[0]

            conn.close()
            total_pages=(total // per_page) + (1 if total % per_page > 0 else 0)
            # Prepare the response with pagination metadata
            response = {
                'users': users,
                'pagination': {
                    'total': total,
                    'page': page,
                    'pages': total_pages,
                    'per_page': per_page,
                    'next_page': f"/staff1?page={page + 1}&per_page={per_page}" if page < total_pages else None,
                    'prev_page': f"/staff1?page={page - 1}&per_page={per_page}" if page > 1 else None,
                }
            }
            print(users)
            return response
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
