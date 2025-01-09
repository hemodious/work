from flask import Blueprint
from services.staff_services import *
from flask_jwt_extended import jwt_required,get_jwt_identity
from constants.HTTP_STATUS_CODES import *
staff=Blueprint('staff',__name__)
@staff.route('/staff1',methods=['GET'])
def staff1():
    try:
        #fetching complaints for staff1 from database
        data=Staff_services.query_for_staff_1()
        return data,HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR

@staff.route('/staff2',methods=['GET'])
def staff2():
    #fetches complaints for staff2 from the database
    try:
        data=Staff_services.query_for_staff_2()
        return data,HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR


@staff.route('/login', methods=['POST'])
def login():
    #logs staff in 
    try:
        data=Staff_services.login()
        return data
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR

@staff.route('/register_staff',methods=['POST'])
def register_staff():
    #registers a new staff member
    try:
        data=Staff_services.register_staff()
        return data
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR
@staff.route('/logout')
def logout():
    try:
        data=Staff_services.logout()
        return data, HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR


@staff.route('/dashboard1', methods=['GET'])

def dashboard1():
  try:

    data=Staff_services.dashboard1()
    return data , HTTP_200_OK
  
  except Exception as e:
      return str(e),HTTP_500_INTERNAL_SERVER_ERROR

@staff.route('/dashboard2', methods=['GET'])

def dashboard2():
    # takes staff to dashboard to upon sucessful login and getting an access token
    try:
       
        data=Staff_services.dashboard2()
        return data, HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR

@staff.route('/staff_login',methods=['GET'])
def staff_login():
    # takes the user to the login page
    try:
        data=Staff_services.staff_login()
        return data, HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR
    

@staff.post('/taken/refresh')
@jwt_required(refresh=True)
def refresh():
    #gets user's identity and refreshes the token to keep the user logged in
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), HTTP_200_OK
    
    except Exception as e:
        return str(e),HTTP_500_INTERNAL_SERVER_ERROR