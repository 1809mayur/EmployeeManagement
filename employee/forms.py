from cProfile import label
from flask_wtf import FlaskForm
from sqlalchemy import false
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError,InputRequired
from employee.models import Employee


class EmployeeForm(FlaskForm):
# checking whether email is already exist or not.
    def validate_email(self,user_email_checking):
        email_address = Employee.query.filter_by(email = user_email_checking.data).first()
        if email_address:
            raise ValidationError("Email ID already exist! Please try with new email_adress")

# checking phone number already exist or not.
    def validate_phoneNumber(self,user_phoneNumber_checking):
        phoneNumber = Employee.query.filter_by(phoneNumber = user_phoneNumber_checking.data).first()
        if phoneNumber:
            raise ValidationError("Mobile Number already exist! Try another mobile number")



    firstName = StringField(label = 'First Name',validators=[DataRequired()])
    lastName = StringField(label = 'Last Name',validators=[DataRequired()])
    email = EmailField(label ="Email Address",validators=[DataRequired(), Email()])
    phoneNumber = StringField(label = 'Mobile Number',validators=[DataRequired(),Length(min=10,max=10)])
    dob = StringField(label = 'Date of Birth',validators=[DataRequired(),Length(min=10,max=10)])
    address = StringField(label = 'Address',validators=[DataRequired()])
    submit = SubmitField(label='Create Account')
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=8)])
    confirmPassword = PasswordField(label='Confirm Password',validators=[DataRequired(), EqualTo('password')])
    isAdmin = HiddenField(default="False")

# Login Form.
class LoginForm(FlaskForm):
    email = EmailField(label='Email Adress',validators=[InputRequired(),Email()])
    password = PasswordField(label='Password')
    submit = SubmitField(label='Login')

# Search Form.
class SearchForm(FlaskForm):
    keyword = StringField(label='Search Here')
    submit = SubmitField(label='Search')