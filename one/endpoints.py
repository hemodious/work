from flask import Blueprint,send_file ,request,jsonify,render_template,redirect,url_for, session, flash
from my_module import db_connection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
import random
import string
import datetime
from io import BytesIO
from PIL import Image
import validators
from constants.vars import *
# blueprint to organise my routes or endpoints
api = Blueprint('api', __name__)

#function to get the image from the database
def get_image_data(image_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM user WHERE id = ?",(image_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0]  # Assuming image data is in the first column
    return None



@api.route('/download/<int:image_id>')
# function to convert into downloadable format
def download(image_id):
    # Get the binary image data for the given image_id
    image_data = get_image_data(image_id)
    
    if image_data is None:
        return jsonify({"error": "no image was attached"}), 404
    
    # Create a BytesIO object from the binary data
    image_io = BytesIO(image_data)
    image_io.seek(0)  # Move to the start of the BytesIO object
    
    # Open the image using Pillow
    image = Image.open(image_io)
    
    # Create a new BytesIO stream to save the converted image
    output_io = BytesIO()
    
    # Save the image in the desired format  PNG
    image.save(output_io, format='PNG')  
    output_io.seek(0) # Move to the start of the BytesIO object
    return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='image.png')



@api.route('/user',methods=['GET','POST'])#route to  get all user data/ create  new user
def user():
    conn=db_connection()#opening the database connection
    cursor=conn.cursor()
    if request.method == 'GET':
        cursor= conn.execute("SELECT * FROM user")#querying the table to get all user data
        users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9],status=row[10])
            for row in cursor.fetchall()
        ]#store  the data in a list of dictionaries
        if users is not None:# checking if the data is not empty
            return jsonify(users)
        
    if request.method == 'POST':# if the request is post then we will create a new user
# variables to  store the data from the request
        new_name= request.form['name']
        new_telephone=request.form['telephone']
        new_complaint=request.form['complaint']
        new_email=request.form['email']
        new_category=request.form['category']
        #file handling
        new_image=request.files.get('image')
        #checks if the image is empty or not 
        if  new_image:
            image_data=new_image.read()#gets the image if added
        else:
            image_data=None    
        
        characters=string.ascii_letters+ string.digits*4
        ans=''.join(random.choices(characters, k=7) )
        store=[] 
        for good in store:
         if good == ans :
            return("already exists")
         else:
            store.append(ans)  
            return(ans)   
        new_complaint_id=ans
        update_status="unresolved"
        #inserting the data into the table
        sql="""INSERT INTO user (name,telephone,complaint,email,category,image,complaint_id,status)
        VALUES (?,?,?,?,?,?,?,?)"""
        # executing the query
        cursor=cursor.execute(sql,(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id,update_status))
        conn.commit()
        conn.close()
        #code to send  email to clients
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login("moorleinternship@gmail.com","kocqukrajdvftmyb")
        msg=MIMEMultipart()
        msg['From']="moorleinternship@gmail.com"
        msg['To']=new_email
        msg['Subject']="COMPLAINT"
        #body of message to user
        body=f"Dear {new_name} ,\n\nyour complaint in category {new_category.upper()} has been recieved your complaint ID is {new_complaint_id} ,our staff will contact you soon\n \nThank you "
        msg.attach(MIMEText(body,'plain'))
        server.sendmail("moorleinternship@gmail.com",new_email,msg.as_string())
        server.quit()#closing the server
     #code to send mail to staff
        server2=smtplib.SMTP('smtp.gmail.com',587)
        server2.starttls()
        server2.login("moorleinternship@gmail.com","kocqukrajdvftmyb")
        #email to staff1
        msg=MIMEMultipart()
        msg['From']="moorleinternship@gmail.com"
        msg['To']="affoh.emmanuel.ea@gmail.com"
        msg['Subject']="NEW REPORT"
        #email to staff2
        msg2=MIMEMultipart()
        msg2['From']="moorleinternship@gmail.com"
        msg2['To']="michaelopoku790@gmail.com"
        msg2['Subject']="NEW REPORT"
        body1=f"Dear Emmanuel ,\n\n{new_name},with id \033{new_complaint_id} has  submitted a complaint in \033 category  {new_category.upper()}  ,please contact him/her soon\n\n thank you "
        body2=f"Dear Michael ,\n\n{new_name}, with id \033{new_complaint_id} has  submitted a complaint in \033category {new_category.upper()} ,please contact him/her soon\n\n thank you "
        #a list issues staff one should handle
        checker=["transaction issue","account management issue","security issues"]
        #checking if the complaint is in the list of issues staff1  should handle
        for check in checker:
            if new_category==check:
                msg.attach(MIMEText(body1,'plain'))
                server2.sendmail("moorleinternship@gmail.com","affoh.emmanuel.ea@gmail.com",msg.as_string())#dont forget to change the email
                break
            else:#if  the complaint is not in the list of issues staff1 should handle it passes it to  staff2
                msg2.attach(MIMEText(body2,'plain'))
                server2.sendmail("moorleinternship@gmail.com","michaelopoku790@gmail.com",msg2.as_string())#dont forget to change the email
                break
        server2.quit()
        return redirect(f'/success?complaintId={new_complaint_id}')

   


@api.route('/staff1',methods=['GET'])
#function to query all complaints belonging to staff1 depending on the category
def staff1():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int) 
    offset = (page - 1) * per_page 
    conn=db_connection()
    cursor=conn.cursor()
    issues=('transaction issue','account management issue','security issue')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?) LIMIT ? OFFSET ?',(*issues,per_page,offset))
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=f"/download/{row[0]}",complaint_id=row[9], date=row[11],status=row[10])
            for row in cursor.fetchall()
        ]
   
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
    return jsonify(response)
    



@api.route('/staff2',methods=['GET'])
#function to query all complaints belonging to staff2 depending on the category
def staff2():
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
    return jsonify(response)




@api.route('/login', methods=['POST'])
#function to login a user
def login():
    user_email = request.form['email']
    user_password = request.form['password']
    
    # Authentication logic
    if user_email == "affoh.emmanuel.ea@gmail.com" and user_password == "password":
        session['logged_in'] = True  # Set logged in session
        session['user_email'] = user_email
        return jsonify({
            "message": "Login successful",
            "redirectUrl": url_for('api.dashboard1')  # Redirect to dashboard1
        }), 200
    elif user_email == "michaelopoku790@gmail.com" and user_password == "password":
        session['logged_in'] = True  # Set logged in session
        session['user_email'] = user_email
        return jsonify({
            "message": "Login successful",
            "redirectUrl": url_for('api.dashboard2')  # Redirect to dashboard2
        }), 200
    else:
        return jsonify({
            "message": "Invalid credentials",
        }), 401
    



@api.route('/dashboard1', methods=['GET'])
#function to display dashboard1 depending on the credentials
def dashboard1():
    if not session.get('logged_in'):
        return redirect(url_for('api.staff_login'))  # Redirect to login if not logged in
    return render_template('dashboard1.html')




@api.route('/dashboard2', methods=['GET'])
#function to display dashboard2 depending on the credentials
def dashboard2():
    if not session.get('logged_in'):
        return redirect(url_for('api.staff_login'))  # Redirect to login if not logged in
    return render_template('dashboard2.html')




@api.route('/logout')
#function to logout a user
def logout():
    session.pop('logged_in', None)  # Remove logged in session
    session.pop('user_email', None)  # Remove user email from session
    return redirect(url_for('api.staff_login'))  # Redirect to login page







@api.route('/staff_login',methods=['GET'])
#function to display the staff login page
def staff_login() :
    return render_template('login.html')




@api.route('/update_status', methods=['POST'])
#function to update the status of the the complaint
def update_status():
    conn = db_connection()  # Open the database connection
    cursor = conn.cursor()

    # Get the complaint_id and new_status from the request
    complaint_id = request.form['complaint_id']
    new_status = request.form['status']

    if not new_status:
        new_status="unresolved"

    # Get the current date and time
    current_time = datetime.datetime.now()

    # SQL query to update the status and the timestamp
    sql = """UPDATE user SET status = ?, date = ? WHERE complaint_id = ?"""
    
    # Execute the query
    cursor.execute(sql, (new_status, current_time, complaint_id))
    conn.commit()  # Commit the changes
    conn.close()   # Close the connection
# 
#sends a mail to the customer if the status 
    if new_status ==valid:
        conn = db_connection()  # Open the database connection
        cursor = conn.cursor()
        email_query="SELECT email FROM user WHERE complaint_id = ?"
        cursor.execute(email_query, (complaint_id,))
        email = cursor.fetchone()[0]
        print(email)
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login("moorleinternship@gmail.com","kocqukrajdvftmyb")
        msg=MIMEMultipart()
        msg['From']="moorleinternship@gmail.com"
        msg['To']=email
        msg['Subject']="COMPLAINT RESOLVED"

        #body of message to user
        body=f"Dear Customer ,\n\n {complaint_id} ,your complaint has been resolved\n \nThank you "
        msg.attach(MIMEText(body,'plain'))
        try:
            server.sendmail("moorleinternship@gmail.com",email,msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
        server.quit()#closing the server
        conn.close()  
    return jsonify({"message": "Status updated successfully", "updated_at": current_time.isoformat()}), 200


@api.route('/complaint',methods=['GET'])
# function to display the complaint page
def complaint():
    return render_template("index.html")



@api.route('/success',methods=['GET'])
# function to display the success page
# Get the complaint ID from the query parameters
def success():
    complaint_id = request.args.get('complaintId')
    
    # Fetch the complaint data (if needed)
  
    # Render the success page and pass the complaint ID
    return render_template('success_page.html', complaint_id=complaint_id)
