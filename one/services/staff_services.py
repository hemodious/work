from flask import request,session,url_for,redirect,render_template,jsonify
from my_module import *
from werkzeug.security import generate_password_hash
import validators
from queries.newUser import *
class Staff_services:
    def register_staff():
            
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        hashed_password=generate_password_hash(password)
        
        if not validators.email(email):
            return jsonify({"message": "Invalid email address"}), 400
        
        conn=staff_connection()
        cursor=conn.cursor()
        staff_auth=cursor.execute('SELECT email FROM staff WHERE email= ?',(email,)).fetchone()
        print(staff_auth)
        if staff_auth:
            return jsonify({
                "message":"user alrready exists"
            })
        else:
            query='INSERT INTO staff (username,email,password) VALUES(?,?,?)'
            cursor.execute(query,(name,email,hashed_password))
            conn.commit()
            cursor.close()

            return jsonify({
            "message":"successfully added"
            },hashed_password)
    def login():
        user_email = request.form['email']
        user_password = request.form['password']
        try:
            user= verifyEmail(user_email)
            password= verifyPassword(user_password)
        
        except:
            return jsonify({"error":"Invalid email or password"})
        # Authentication logic
        
        if validators.email(user_email):
            if user and password:
                    session['logged_in'] = True  # Set logged in session
                    session['user_email'] = user_email
                    return jsonify({
                    "message": "Login successful",
                    "redirectUrl": url_for('staff.dashboard1')  # Redirect to dashboard1
            }), 200
            else:
                    return jsonify({
                        "message": "Login unsuccessful,wrong password",
                    })
    def query_for_staff_1():
         
            try:
                data=UserQuery.queryforstaff1()
                print (data)
                if data is None:
                    return jsonify({"no data returned from query"})
                else:
                    return data
                
            except:
                return jsonify({"error":"An error occurred while fetching user data"})

    def query_for_staff_2():
       
        try:
            data=UserQuery.queryforstaff2()
            print({"message":data})
            if data is None:
                return jsonify({"error": "No data returned from query"})
            return jsonify(data)
        except:
            return jsonify({"error":"An error occurred while fetching user data"})
        
    def logout():
        session.pop('logged_in', None)  # Remove logged in session
        session.pop('user_email', None)  # Remove user email from session
        return redirect(url_for('staff.staff_login'))  # Redirect to login page

    def dashboard1():
        if not session.get('logged_in'):
            return redirect(url_for('staff.staff_login'))  # Redirect to login if not logged in
        return render_template('dashboard1.html')
    def staff_login() :
        return render_template('login.html')
    
    def dashboard2():
        if not session.get('logged_in'):
            return redirect(url_for('api.staff_login'))  # Redirect to login if not logged in
        return render_template('dashboard2.html')