from queries.newUser import UserQuery
from flask import Flask, request
from services.user_services import *
class user_controller:
    def __init__(self):
        pass
    def get_all_user(self):
       data= UserQuery.queryforall()
       return data
    
    def create_new_user():
        user = User_services.create_user()
        return user
    
    
