import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
from flask import jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from constants.vars import *

def db_connection():
    conn =None
    try:
        conn = sqlite3.connect('user.sqlite')
        conn.row_factory = sqlite3.Row 
    except sqlite3.error as e:
        print(e)
    return conn

def staff_connection():
    conn =None
    try:
        conn = sqlite3.connect('staff.db')
    except sqlite3.error as e:
        print(e)
    return conn

def MailToClient(new_email,new_category,new_name ,new_complaint_id):
    try:
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
    except:
        return jsonify({"error":"cant send mail"})
    


def MailTOStaff(new_name,new_complaint_id,new_category):
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


def get_image_data(image_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM user WHERE id = ?", (image_id,))
        row = cursor.fetchone()
        conn.close()
    
        if row:
         return row[0]  # Assuming image data is in the first column
        else:
            return None
    except:
        return jsonify({"error":"error retrieving image"})
    
def successmail(complaint_id):
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
def verifyEmail(email):
    try:
        conn = staff_connection()  # Open the database connection
        cursor = conn.cursor()
        email_query="SELECT email FROM staff WHERE email = ?"
        cursor.execute(email_query, (email,))
        fin = cursor.fetchone()[0]
        if fin is None:
            return {"no email found"}

        return fin

    except:
        return jsonify({"error":"error verifying email"})
    
def verifyPassword(password):
    try:
        conn = staff_connection()  # Open the database connection
        cursor = conn.cursor()
        email_query="SELECT password FROM staff WHERE password = ?"
        cursor.execute(email_query, (password,))
        fin = cursor.fetchone()[0]
        if fin is None:
            return {"invalid password"}

        check_password_hash(fin,password)
        return fin

    except:
        return {"error":"error verifying password"}
   
