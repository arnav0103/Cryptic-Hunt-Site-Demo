from cryptic import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String(64),index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    classe = db.Column(db.String)
    password_hash = db.Column(db.String)
    question = db.Column(db.Integer)
    def __init__(self,email,username,password,question,fname,lname, classe):
        self.fname=fname
        self.lname=lname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.question = question
        self.classe = classe

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
