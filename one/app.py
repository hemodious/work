from flask import Flask ,request,jsonify,render_template
import json
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
import random
import string

app = Flask(__name__)

#databasee connection
def db_connection():
    conn =None
    try:
        conn = sqlite3.connect('user.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/user',methods=['GET','POST'])#route to  get all user data/ create  new user
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
        #inserting the data into the table
        sql="""INSERT INTO user (name,telephone,complaint,email,category,image,complaint_id)
        VALUES (?,?,?,?,?,?,?)"""

        # executing the query

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

        #body of message to user

        body=f"Dear {new_name} ,your complaint in \033category {new_category} has been recieved your complaint ID is \033{new_complaint_id} ,our staff will contact you soon\n \nThank you "
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
        body1=f"Dear Emmanuel ,{new_name},with id \033{new_complaint_id} has  submitted a complaint in \033 category {new_category},please contact him/her soon\n thank you "
        body2=f"Dear Michael ,{new_name}, with id \033{new_complaint_id} has  submitted a complaint in \033category {new_category} ,please contact him/her soon\n thank you "
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
       

@app.route('/staff1',methods=['GET'])
def staff1():
    conn=db_connection()
    cursor=conn.cursor()
    issues=('transaction issue','account management issue','security issue')
    cursor.execute('SELECT * FROM user WHERE category IN  (?,?,?)',issues)
    users=[
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[9])
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
            dict(id=row[0],name=row[1],telephone=row[2],complaint=row[3],email=row[4],category=row[5],image=[6],complaint_id=row[9])
            for row in cursor.fetchall()
        ]
    return users



@app.route('/login',methods=['POST'])
#authenticate staff upon login
def  login():
    user_email=request.form['email']
    user_password=request.form['password']
    if user_email== "affoh.emmanuel.ea@gmail.com" and user_password=="password":
        return "login successful",#render_template('staff1.html')
    elif user_email== "affoh.emmanuel.ea@gmail.com" and user_password!="password":
        return "invalid password"
    elif user_email == "michaelopoku790@gmail.com" and user_password=="password":
         return "login successful",#render_template('staff2.html')
    elif user_email  == "michaelopoku790@gmail.com" and user_password!="password":
        return "invalid password"
    else : 
        return "invalid credentials"





if __name__ == '__main__':
    app.run(debug=True)