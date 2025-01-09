from my_module import *
from flask import request
class Staff():
    def queryforstaff2():
        #function to query all complaints belonging to staff2 depending on the category
   
        page =request.args.get('page',1,type=int)
        per_page= request.args.get('per_page',10,type=int)
        offset = (page - 1) * per_page
        conn=db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?) LIMIT ? OFFSET ?',(*ISSUES2,per_page,offset))
        users=[
                dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10] )
                for row in cursor.fetchall()
            ]
        
        cursor.execute('SELECT COUNT(*) FROM user WHERE category IN (?,?,?)',ISSUES1)
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
        return response
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
                cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?) LIMIT ? OFFSET ?',(*ISSUES,per_page,offset))
                users=[
                    dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10])
                    for row in cursor.fetchall()
                ]
                if users is None:
                     return jsonify({"message": "No users found"}), 404
            except sqlite3.Error as e:
                 return jsonify({"message": "Database query failed"}), 500
           
            cursor.execute('''
                SELECT COUNT(*) FROM user 
                WHERE category IN (?, ?, ?)
            ''', ISSUES)
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
            return response
        except:
                return jsonify({"error": "An error occurred couldn't query database"}), 500
        
    def get_staff(email):
       try:
        conn = staff_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff WHERE email=?", (email,))
        row = cursor.fetchone()
        
        if row is not None:
            staff = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'password': row[3]
            }
            return staff
        else:
            return None  # No staff found with the given email
        
       except Exception as e:
            return None  # Return None or handle the error as needed
        
       finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()