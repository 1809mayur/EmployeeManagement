from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import secrets

app = Flask(__name__)

db = SQLAlchemy(app)

ma = Marshmallow(app)

secretKey = secrets.token_hex(16)
app.config["SECRET_KEY"] = secretKey



# setting up sqlite database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
