from flask import request,session,url_for,redirect,render_template,jsonify
from my_module import *
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,create_refresh_token
import validators
from queries.newUser import *
from constants.vars import *
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
        staff_auth
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
                    user=UserQuery.get_staff(user_email)
                    user_data={
                        "id":user["id"],
                        "name":user["name"],
                        "email":user["email"],
                    }
                    print(user)
                    access_token = create_access_token(identity=(str(user["id"])))
                    refresh_token= create_refresh_token(identity=(str(user["id"])))
                    session['logged_in'] = True  # Set logged in session
                    session['user_email'] = user_email
                    
                    if user["email"]== staff_1:
                        return jsonify({
                        "message": "Login successful",
                        "redirectUrl": url_for('staff.dashboard1'),
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user_data": user_data
                    }), 200

                    elif user["email"]== staff_2:
                        return jsonify({
                            "message": "Login successful",
                            "redirectUrl": url_for('staff.dashboard2'),
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "user_data": user_data
                        }), 200

                    else:
                        return jsonify({"message": "Invalid staff"}), 401
                
            
                
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
