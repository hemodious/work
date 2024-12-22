from flask import Blueprint,send_file ,request,jsonify,render_template,redirect,url_for, session, flash
from my_module import db_connection
from my_module import MailToClient
from my_module import MailTOStaff
from my_module import successmail
from my_module import get_image_data
from my_module import verifyEmail,verifyPassword
from variables import staff2,staff1
from queries import newUser
from queries.newUser import UserQuery
import random
import string
import datetime
from io import BytesIO
from PIL import Image

# blueprint to organise my routes or endpoints
api = Blueprint('api', __name__)

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
    
    if request.method == 'GET':
       data=UserQuery.queryforall()
       return jsonify(data)
        
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
        for goods in store:
         if goods == ans :
            return("already exists")
         else:
            store.append(ans)  
            return(ans)   
        new_complaint_id=ans
        update_status="unresolved"
        #inserting the data into the table
        UserQuery.createNewUser(new_name,new_telephone,new_complaint,new_email,new_category,image_data,new_complaint_id,update_status)
        #code to send  email to clients
        MailToClient(new_email,new_category,new_name,new_complaint_id)
     #code to send mail to staff
        MailTOStaff(new_name,new_complaint,new_category)
        return redirect(f'/success?complaintId={new_complaint_id}')

   


@api.route('/staff1',methods=['GET'])
#function to query all complaints belonging to staff1 depending on the category
def staff1():
  try:
   data=UserQuery.queryforstaff1()
   if data is None:
       return jsonify({"no data returned from query"})
   else:
       return jsonify(data)
    
  except:
    return jsonify({"error":"An error occurred while fetching user data"})


@api.route('/staff2',methods=['GET'])
#function to query all complaints belonging to staff2 depending on the category
def staff2():
    try:
        data=UserQuery.queryforstaff2()
        if data is None:
            return jsonify({"error": "No data returned from query"})
        return jsonify(data)
    except:
        return jsonify({"error":"An error occurred while fetching user data"})
    
    

@api.route('/login', methods=['POST'])
#function to login a user
def login():
    user_email = request.form['email']
    user_password = request.form['password']
    try:
       user= verifyEmail(user_email)
       password= verifyPassword(user_email)
      
    except:
        return jsonify({"error":"Invalid email or password"})
    # Authentication logic
    if user ==staff1 and user_password == password:
        try:
            session['logged_in'] = True  # Set logged in session
            session['user_email'] = user_email
            return jsonify({
            "message": "Login successful",
            "redirectUrl": url_for('api.dashboard1')  # Redirect to dashboard1
         }), 200
        except:
            print("error loading page")
    elif user== staff2 and user_password==password:
            session['logged_in'] = True  # Set logged in sessionn
            session['user_email'] = user
            return jsonify({
            "message": "Login successful",
            "redirectUrl": url_for('api.dashboard2')  # Redirect to dashboard1
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
    if new_status =="resolved":
        successmail(complaint_id)
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
