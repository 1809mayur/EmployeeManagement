
from .models import Students
from flask import jsonify
from api import app






@app.route('/')
def home():
    return "<h1> Hello JI </h1>"

@app.routes('/api', methods="GET")
def api():
    students = Students.query.all()
    
    
