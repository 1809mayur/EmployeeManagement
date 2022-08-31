
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
import os


# flask is instantiated as an app.
app = Flask(__name__)


# sqlalchemy instance for database related stuffs.
db = SQLAlchemy(app)

# Initialising Marshmallow.
ma = Marshmallow(app)

# Initialising Bcrypt to generate hash of password.
bcrypt = Bcrypt(app)

# Initialising LOGIN MANAGER.
login_manager = LoginManager(app)

login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# SECRET KEY.
app.config["SECRET_KEY"] = "6798ff58efe3cd907bfa5233"

# Base Directory.
basedir = os.path.abspath(os.path.dirname(__file__))

# setting up sqlite database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,'employeeData.db')


