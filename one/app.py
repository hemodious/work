from flask import Flask ,request,jsonify
import json
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
import random
import string

app = Flask(__name__)


def db_connection():
    conn =None
    try:
        conn = sqlite3.connect('user.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/user',methods=['GET','POST'])
def user():
    conn=db_connection()
    cursor=conn.cursor()
    if request.method == 'GET':
        cursor= conn.execute("SELECT * FROM user")
        users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[7])
            for row in cursor.fetchall()
        ]

        if users is not None:
            return jsonify(users)
        

    if request.method == 'POST':
        new_name= request.form['name']
        new_telephone=request.form['telephone']
        new_complaint=request.form['complaint']
        new_email=request.form['email']
        new_category=request.form['category']
        new_image=request.files['image']
        image_data = new_image.read() 
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
        sql="""INSERT INTO user (name,telephone,complaint,email,category,image,complaint_id)
        VALUES (?,?,?,?,?,?,?)"""
        
        cursor=cursor.execute(sql,(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id))
        conn.commit()
        #code to send  email to clients
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login("moorleinternship@gmail.com","kocqukrajdvftmyb")
        msg=MIMEMultipart()
        msg['From']="moorleinternship@gmail.com"
        msg['To']=new_email
        msg['Subject']="COMPLAINT"
        body=f"Dear {new_name} ,your complaint in \033category {new_category} has been recieved your complaint ID is \033{new_complaint_id} ,our staff will contact you soon\n thank you "
        msg.attach(MIMEText(body,'plain'))
        server.sendmail("moorleinternship@gmail.com",new_email,msg.as_string())
        server.quit()

     #code to send mail to staff
        server2=smtplib.SMTP('smtp.gmail.com',587)
        server2.starttls()
        server2.login("moorleinternship@gmail.com","kocqukrajdvftmyb")
        msg=MIMEMultipart()
        msg['From']="moorleinternship@gmail.com"
        msg['To']="affoh.emmanuel.ea@gmail.com"
        msg['Subject']="NEW REPORT"

        msg2=MIMEMultipart()
        msg2['From']="moorleinternship@gmail.com"
        msg2['To']="michaelopoku790@gmail.com"
        msg2['Subject']="NEW REPORT"
        body1=f"Dear Emmanuel ,{new_name},with id \033{new_complaint_id} has  submitted a complaint in \033 category {new_category},please contact him/her soon\n thank you "
        body2=f"Dear Michael ,{new_name}, with id \033{new_complaint_id} has  submitted a complaint in \033category {new_category} ,please contact him/her soon\n thank you "
        #a list issues staff one should handle
        checker=["transaction issue","account management issue","security issues"]
        for check in checker:
            if new_category==check:
                msg.attach(MIMEText(body1,'plain'))
                server2.sendmail("moorleinternship@gmail.com","affoh.emmanuel.ea@gmail.com",msg.as_string())#dont forget to change the email
                break
            else:
                msg2.attach(MIMEText(body2,'plain'))
                server2.sendmail("moorleinternship@gmail.com","michaelopoku790@gmail.com",msg2.as_string())#dont forget to change the email
                break
        server2.quit()
       
       
    return jsonify({"complaint ID":new_complaint_id}),201
       

@app.route('/staff1',methods=['GET'])
def staff1():
    conn=db_connection()
    cursor=conn.cursor()
    issues=('transaction issue','account management issue','security issue')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[7])
            for row in cursor.fetchall()
        ]
    return users

@app.route('/staff2',methods=['GET'])
def staff2():
    conn=db_connection()
    cursor=conn.cursor()
    issues=('crash issue','perfomance management issue','others')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[7])
            for row in cursor.fetchall()
        ]
    return users



@app.route('/login',methods=['POST'])
def  login():
    user_email=request.form['email']
    user_password=request.form['password']
    if user_email== "affoh.emmanuel.ea@gmail.com" and user_password=="password":
        return "login successful"
    elif user_email== "affoh.emmanuel.ea@gmail.com" and user_password!="password":
        return "invalid password"
    elif user_email == "michaelopoku790@gmail.com" and user_password=="password":
         return "login successful"
    elif user_email  == "michaelopoku790@gmail.com" and user_password!="password":
        return "invalid password"
    else : 
        return "invalid credentials"





if __name__ == '__main__':
    app.run(debug=True)