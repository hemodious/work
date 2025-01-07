from flask import Blueprint
from services.staff_services import *
from flask_jwt_extended import jwt_required,get_jwt_identity
from constants.HTTP_STATUS_CODES import *
staff=Blueprint('staff',__name__)
@staff.route('/staff1',methods=['GET'])
def staff1():
    data=Staff_services.query_for_staff_1()
    return data,HTTP_200_OK

@staff.route('/staff2',methods=['GET'])
def staff2():
    data=Staff_services.query_for_staff_2()
    return data,HTTP_200_OK

@staff.route('/login', methods=['POST'])
def login():
    data=Staff_services.login()
    return data, HTTP_200_OK

@staff.route('/register_staff',methods=['POST'])
def register_staff():
    data=Staff_services.register_staff()
    return data
@staff.route('/logout')
def logout():
    data=Staff_services.logout()
    return data, HTTP_200_OK


@staff.route('/dashboard1', methods=['GET'])
@jwt_required()
def dashboard1():
    current_user = get_jwt_identity()
    data=Staff_services.dashboard1()
    return data, HTTP_200_OK

@staff.route('/dashboard2', methods=['GET'])
@jwt_required()
def dashboard2():
    current_user = get_jwt_identity()
    data=Staff_services.dashboard2()
    return data, HTTP_200_OK

@staff.route('/staff_login',methods=['GET'])
def staff_login():
    data=Staff_services.staff_login()
    return data, HTTP_200_OK

@staff.post('/taken/refresh')
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), HTTP_200_OK
    