from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#creating an instance
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///TutorGate.db'
app.config['SECRET_KEY']='5c7802c866f41bb9d34626ef'
app.config['UPLOAD_FOLDER']='/static/files'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
from TutorGate import routes