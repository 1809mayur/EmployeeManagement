
from employee import db
from flask_login import UserMixin

class Employee(UserMixin,db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    firstName = db.Column(db.String(length = 100),nullable =False)
    lastName = db.Column(db.String(length = 100),nullable =False)
    email = db.Column(db.String(length = 100),nullable =False,unique = True)
    phoneNumber = db.Column(db.String(length = 100),nullable =False,unique=True)
    dob = db.Column(db.String(length = 100),nullable =False)
    address = db.Column(db.String(length = 200),nullable = False)
    password = db.Column(db.String(300), nullable=False)
    isAdmin = db.Column(db.String(10),nullable=False )

    def __repr__(self):
        return self.firstName
        
