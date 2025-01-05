from flask import Blueprint
from services.staff_services import *
staff=Blueprint('staff',__name__)
@staff.route('/staff1',methods=['GET'])
def staff1():
    data=Staff_services.query_for_staff_1()
    return data

@staff.route('/staff2',methods=['GET'])
def staff2():
    Staff_services.query_for_staff_2()

@staff.route('/login', methods=['POST'])
def login():
    Staff_services.login()

@staff.route('/register_staff',methods=['POST'])
def register_staff():
    data=Staff_services.register_staff()
    return data
@staff.route('/logout')
def logout():
    Staff_services.logout()

@staff.route('/dashboard1', methods=['GET'])
def dashboard1():
    Staff_services.dashboard1()

@staff.route('/dashboard2', methods=['GET'])
def dashboard2():
    Staff_services.dashboard2()

@staff.route('/staff_login',methods=['GET'])
def staff_login():
    Staff_services.staff_login()
    