from my_module import *
from flask import request,send_file,redirect,render_template
import random
from queries.newUser import *
import string
import datetime
from io import BytesIO
from PIL import Image
class User_services:
    def create_user():
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
    
    def get_all_users():
        return UserQuery.queryforall()
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
        if new_status ==VALID:
            successmail(complaint_id)
        return jsonify({"message": "Status updated successfully", "updated_at": current_time.isoformat()}), 200

    
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

    
    def success():
        complaint_id = request.args.get('complaintId')
        
        # Fetch the complaint data (if needed)
    
        # Render the success page and pass the complaint ID
        return render_template('success_page.html', complaint_id=complaint_id)

