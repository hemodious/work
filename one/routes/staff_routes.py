from flask import Blueprint
from services.staff_services import *
staff=Blueprint('staff',__name__)
@staff.route('/staff1',methods=['GET'])
def staff1():
    data=Staff_services.query_for_staff_1()
    return data

@staff.route('/staff2',methods=['GET'])
def staff2():
    data=Staff_services.query_for_staff_2()
    return data

@staff.route('/login', methods=['POST'])
def login():
    data=Staff_services.login()
    return data

@staff.route('/register_staff',methods=['POST'])
def register_staff():
    data=Staff_services.register_staff()
    return data
@staff.route('/logout')
def logout():
    data=Staff_services.logout()
    return data


@staff.route('/dashboard1', methods=['GET'])
def dashboard1():
    data=Staff_services.dashboard1()
    return data

@staff.route('/dashboard2', methods=['GET'])
def dashboard2():
    data=Staff_services.dashboard2()
    return data

@staff.route('/staff_login',methods=['GET'])
def staff_login():
    data=Staff_services.staff_login()
    return data
    