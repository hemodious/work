from flask import Blueprint ,request,jsonify,render_template,redirect,url_for
#databasee connection
from my_module import db_connection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
from  my_module import chat_connection
import random
import string

def gene_pss():
     characters=string.ascii_letters+ string.digits*4

     ans=''.join(random.choices(characters, k=7) )
     store=[] 
     for good in store:
         if good == ans :
            return("already exists")
         else:
            store.append(ans)  
            return(ans)   

api = Blueprint('api', __name__)
@api.route('/user',methods=['GET','POST'])#route to  get all user data/ create  new user
def user():
    conn=db_connection()#opening the database connection
    cursor=conn.cursor()
    if request.method == 'GET':
        cursor= conn.execute("SELECT * FROM user")#querying the table to get all user data
        users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[9])
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
        
        
        new_complaint_id=gene_pss()
    
        #inserting the data into the table
        sql="""INSERT INTO user (name,telephone,complaint,email,category,image,complaint_id)
        VALUES (?,?,?,?,?,?,?)"""

        # executing the query

        cursor=cursor.execute(sql,(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id))
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
       
       
    return jsonify({"complaint ID":new_complaint_id}),201
       

@api.route('/staff1',methods=['GET'])
def staff1():
    conn=db_connection()
    cursor=conn.cursor()
    issues=('transaction issue','account management issue','security issue')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[9])
            for row in cursor.fetchall()
        ]
    conn.close()
    return jsonify(users)
    
@api.route('/staff2',methods=['GET'])
def staff2():
    conn=db_connection()
    cursor=conn.cursor()
    issues=('crash issue','perfomance management issue','others')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[9])
            for row in cursor.fetchall()
        ]
    return jsonify(users)



@api.route('/login',methods=['POST'])
#authenticate staff upon login
def  login():
    user_email=request.form['email']
    user_password=request.form['password']
    if user_email== "affoh.emmanuel.ea@gmail.com" and user_password=="password":
       return jsonify({
            "message": "Login successful",
            "redirectUrl": "https://customer-complaint.onrender.com/dashboard1"  # URL to redirect to
        }), 200
    elif user_email== "affoh.emmanuel.ea@gmail.com" and user_password!="password":
        return jsonify({
            "message": "invalid password",
                }), 200
    elif user_email == "michaelopoku790@gmail.com" and user_password=="password":
          return jsonify({
            "message": "Login successful",
            "redirectUrl": "https://customer-complaint.onrender.com/dashboard2"  # URL to redirect to
        }), 200
    elif user_email  == "michaelopoku790@gmail.com" and user_password!="password":
        return jsonify({
            "message": "invalid password",
                }), 200
    else : 
        return jsonify({
            "message": "invalid password",
                }), 200

@api.route('/dashboard1',methods=['GET'])
def dashboard1():
    return render_template('dashboard1.html')
@api.route('/dashboard2',methods=['GET'])
def dashboard2():
    return render_template('dashboard2.html')
def  chatroom_login():
    Password=request.form['password']
    if Password=="password":
        return chatroom()
@api.route('/st',methods=['GET'])
def stff_login():
    return render_template('login.html')    
        
@api.route('/chatlogin',methods=['GET'])#sends the staff to the chatroomlogin page
def Login():
    return render_template('chatlogin.html')

@api.route('/chatroom',methods=['GET'])#sends the staff to the chatroom
def chatroom():
    return render_template('chatroom.html')

@api.route('/chatroom_messages',methods=['GET'])
def get_messages():
    conn = chat_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, message FROM chat_messages')
    messages = cursor.fetchall()
    message_list= [{'username': msg[0], 'message': msg[1]} for msg in messages]
    return jsonify(message_list), 200
def staff_login() :
    return render_template('login.html')