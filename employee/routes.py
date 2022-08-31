
from flask import redirect, render_template,request, url_for, flash,get_flashed_messages,jsonify,session
from employee import app, db, bcrypt, login_manager
from flask_bcrypt import generate_password_hash
from employee.models import Employee 
from employee.forms import EmployeeForm, LoginForm, SearchForm
from employee.api import singleEmployeeSchema,allEmployeeSchema
import requests
from flask_marshmallow.fields import URLFor
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,)
from werkzeug.routing import BuildError
from flask_bcrypt import bcrypt,check_password_hash
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)
from datetime import timedelta

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

'''
        ROUTE FOR HOME URL AND ITS VIEW
                                                            '''
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

'''
        ROUTE FOR REGISTRATION URL AND ITS VIEW
                                                            '''
@app.route('/register',methods=['GET','POST'])
def register():
    form = EmployeeForm()

    if form.validate_on_submit():
        try:
            empDetail = Employee(
                firstName = form.firstName.data.lower(),
                lastName = form.lastName.data.lower(),
                email = form.email.data.lower(),
                phoneNumber = form.phoneNumber.data,
                dob = form.dob.data,
                address = form.address.data.lower(),
                password = generate_password_hash(form.password.data),
                isAdmin = form.isAdmin.data.lower()
            )
            
            db.session.add(empDetail)
            db.session.commit()
            flash("employee registered!",category='success')
            return redirect(url_for('login'))
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!",category= "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.",category="warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry",category= "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", category="danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", category="danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", category="danger")

    
    if form.errors != {} :
        for errorMessage in form.errors.values():
            flash( f'{ errorMessage[0]}', category='danger')
    
    return render_template('./accounts/register.html', form = form)

'''
            ROUTE FOR LOGIN FORM AND ITS VIEW                    
                                                        '''
@app.route('/login',methods =['POST','GET'])
def login():
    loginForm = LoginForm()
    
    if loginForm.validate_on_submit():
        try:
            user = Employee.query.filter_by(email= loginForm.email.data.lower()).first()
            if user is None:
                flash(f"Email does not exist, Please register yourself",category="danger")
                return redirect('register')
            else:
                if check_password_hash(user.password,loginForm.password.data):
                    session["id"] = user.id
                    login_user(user)
                    if user.isAdmin == 'false':
                        flash(f"logged In !",category="success")
                        return redirect(url_for('profile',name =user.firstName,id = user.id))
                    else:
                        flash(f"logged In !",category="success")
                        return redirect(url_for('admin',id=user.id))
                else:
                    flash(f"Invalid password",category='danger')
        except Exception as e:
            flash(f"{e}",category='danger')
        
    return render_template('./accounts/login.html',loginForm=loginForm)

@app.route('/<string:name>/<int:id>')
@login_required
def profile(name,id):
    userData = Employee.query.get(id)
    isEdit = False

    if userData is None:
        flash(f"You are not in our databse",category="warning")
        return redirect(url_for('register'))

# Restricting user to see their own profile.
    if session['id'] != id:
        logout_user()
        session['id'] = None
        flash(f"This is not your profile.Kindly log in again! ",category='danger')
        loginForm = LoginForm()
        return render_template('./accounts/login.html',loginForm=loginForm)
    else:
        return render_template('./employee.html',data=userData,isEdit = isEdit)

@app.route('/logout')
@login_required
def logout():
    session['id'] = None
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/delete/<int:adminId>/<int:id>')
@login_required
def delete(adminId,id):
    data = Employee.query.get(id)
    if data.isAdmin:
        if data is None:
            flash(f"Employee does not found in database",category="danger")
        else:
            db.session.delete(data)
            db.session.commit()
            flash(f"Data is removed successfully!",category="success")
            return redirect(url_for('admin',id=adminId))
    
    return render_template("./employee.html",data=data)

'''
    ROUTE FOR ADMIN PANEL.ITS HOME.
                                                        '''
@app.route('/admin/profile/<int:id>')
@login_required
def admin(id):
    form = SearchForm()
    keyword = str()
    
    data = Employee.query.get(id)
    employeeData = Employee.query.all()
    # confirming 'keyword' as an arguement present in our request or not.
    if 'keyword' in request.args:
        keyword =  request.args['keyword']

    param = {'name':keyword}
    apiResponse = requests.get("http://localhost:5000/apiSearch",params=param)
    searchEmployeeData = apiResponse.json()
    

    if len(searchEmployeeData) > 0 :
        return render_template('./admin/adminHome.html',employeeData = searchEmployeeData,form=form,data=data)

    
    if current_user.id == id and data is not None and data.isAdmin == 'true':
        return render_template('./admin/adminHome.html',employeeData=employeeData,form=form,data=data)
    else:
        flash(f"Do not credentials to access this page!",category="danger")
        session['id'] = None
        logout_user()
        return redirect(url_for('login'))

'''
        ROUTE FOR EACH EMPLOYEE DEATAIL PAGE IN ADMIN PANEL.
                                                             '''
@app.route('/admin/<int:adminId>/<int:id>')
@login_required  
def employeeDetail(adminId,id):
    data = Employee.query.get(id)
    adminId = adminId
    return render_template('./admin/employeeDetail.html',data = data,adminId=adminId)


'''
    FROM HERE API ROUTING STARTS WITH ITS VIEWS.

                                                                '''


@app.route('/api',methods=['GET'])
def apiGet():
    allEmployee = Employee.query.all()
    data = jsonify(allEmployeeSchema.dump(allEmployee))
    
    return data


@app.route('/api',methods=['POST'])
def apiPost():

    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    phoneNumber = request.json['phoneNumber']
    address = request.json['address']
    dob = request.json['dob']

    addEmployee = Employee(
                            firstName = firstName,
                            lastName = lastName,
                            email = email,
                            phoneNumber = phoneNumber,
                            address = address,
                            dob = dob
                            )

    db.session.add(addEmployee)
    db.session.commit()

    return singleEmployeeSchema.jsonify(addEmployee)



@app.route('/api/<int:id>',methods = ['PUT','DELETE','GET'])
def apiPutDelete(id):
    data = Employee.query.get(id)

    if request.method == 'DELETE':
        if data is None:
            return jsonify(f"This id : {id} does not exist in our database")
        else:
            db.session.delete(data)

            db.session.commit()

    if request.method == 'PUT':
        if 'firstName' in request.json:
            firstName = request.json['firstName']
        if 'lastName' in request.json:
            lastName = request.json['lastName']
        if 'email' in request.json:
            email = request.json['email']
        if 'phoneNumber' in request.json:
            phoneNumber = request.json['phoneNumber']
        if 'dob' in request.json:
            dob = request.json['dob']
        if 'address' in request.json:
            address = request.json['address']

    return jsonify(singleEmployeeSchema.dump(data))

# Api for searching data inside database based on first name.
@app.route('/apiSearch',methods=['GET'])
def searchApi():
    name = str()
    if 'name' in request.args:
        name = request.args['name'].lower()
        data = Employee.query.filter_by(firstName = name)
        return jsonify(allEmployeeSchema.dump(data))
    
    return jsonify(f"Does not found Parameters! Please pass them.")


@app.route('/hello')
def hello():
    # r = requests.get("http://localhost:5000/api")
    https_url = URLFor('apiGet', values=dict(id='<id>', _scheme='https', _external=True))
    print(https_url)
    
    return render_template('./accounts/home.html')