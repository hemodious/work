from flask import Blueprint,request,render_template
from services.user_services import *
from constants.HTTP_STATUS_CODES import *
from constants.vars import *

# blueprint to organise my routes or endpoints
user = Blueprint('user', __name__)

@user.route('/download/<int:image_id>')
# function to convert into downloadable format
def download_image(image_id):
    data=User_services.download(image_id)
    return data


@user.route('/user',methods=['POST','GET'])#route to  get all user data/ create  new user
def create_user():
  if request.method == 'POST':
    data=User_services.create_user()
    return data
  if request.method == 'GET':
     data=User_services.get_all_users()
     return data




@user.route('/update_status', methods=['POST'])
#function to update the status of the the complaint
def update_status():
   data=User_services.update_status()
   return data

@user.route('/complaint',methods=['GET'])
# function to display the complaint page
def complaint():
    return render_template("index.html")



@user.route('/success',methods=['GET'])
# function to display the success page
# Get the complaint ID from the query parameters
def success():
    data=User_services.success()
    return data

@user.route('/',methods=['GET'])
# function to display the complaint page
def index():
    return render_template("index.html")
