
from flask_cors import CORS
from flask import Flask,jsonify
from routes.staff_routes import staff
from routes.user_routes import user
from routes.error_routes import error
from flask_jwt_extended import JWTManager
from constants.HTTP_STATUS_CODES import *

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
CORS(app)
JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(staff)
app.register_blueprint(user)
app.register_blueprint(error)


app.errorhandler(HTTP_404_PAGE_NOT_FOUND)
def internal_server_error(e):
    return jsonify({"Error_message":"the page you are looking for does not exist"}),HTTP_404_PAGE_NOT_FOUND
if __name__ == '__main__':
   app.run(debug=True)