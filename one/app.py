
from flask_cors import CORS
from flask import Flask
from routes.staff_routes import staff
from routes.user_routes import user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(staff)
app.register_blueprint(user)





if __name__ == '__main__':
   app.run(debug=True)