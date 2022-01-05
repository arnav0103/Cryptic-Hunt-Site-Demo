import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo

login_manager = LoginManager()
app =  Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zchimkopsxnfah:fd83305e202c3027c13220b224648cd27be7b5d8b2fbb22c258a4b48a86a24c3@ec2-54-172-219-6.compute-1.amazonaws.com:5432/d46q4o48htr57r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MONGO_URI"] = "mongodb+srv://Arnav:arnavgupta0103@cluster0.ntgb4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'
