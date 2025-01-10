from flask import Blueprint,jsonify
from constants.HTTP_STATUS_CODES import *
error= Blueprint('error',__name__)

error.errorhandler(HTTP_400_BAD_REQUEST)
def bad_request(e):
    return jsonify({"Error_message":"you've made a bad request"}),HTTP_400_BAD_REQUEST

error.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return jsonify({"Error_message":"there is a problem with the server"}),HTTP_500_INTERNAL_SERVER_ERROR


error.app_errorhandler(HTTP_404_PAGE_NOT_FOUND)
def page_not_found(e):
    return jsonify({"Error_message":"the page you are looking for does not exist"}),HTTP_404_PAGE_NOT_FOUND