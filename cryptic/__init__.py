import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
import dns

login_manager = LoginManager()
app =  Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MONGO_URI"] = "mongodb+srv://Arnav:arnavgupta0103@cluster0.ntgb4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'
