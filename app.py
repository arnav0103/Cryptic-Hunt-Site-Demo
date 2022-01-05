from cryptic import app,db,mongo
from flask import render_template,redirect,url_for,request,flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from cryptic.models import User,Logs
from cryptic.forms import LoginForm,RegistrationForm,PlayForm
from sqlalchemy import desc , asc
from werkzeug.security import generate_password_hash,check_password_hash
username =''
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('login_popup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    mess = 'Please fill form to login'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        try:
            if user.check_password(form.password.data) and user is not None:
                #Log in the user

                login_user(user)
                mess = 'Logged in successfully.'
                current_user = user

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0]=='/':
                    next = url_for('welcome_user')
                return redirect(next)
        except AttributeError:
            mess = 'No such login.Pls register to make an account '
    return render_template('Login.html', form=form,mess=mess)

@app.route('/register',methods=['GET','POST'])
def register():
    mess = 'Register to play the most exciting cryptic hunts ever'
    try:
        form = RegistrationForm()
        email = form.email.data
        username = form.username.data
        password = form.password.data
        fname = form.fname.data
        lname = form.lname.data
        classe = form.classe.data

        if form.validate_on_submit():
            user = User(email,username,password,1,fname,lname, classe)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    except :
        mess = 'username already been used'
    return render_template('Register.html',form = form,mess=mess)
@app.route('/play',methods=['GET','POST'])
@login_required
def play():
    if current_user.restricted=="Yes":
        abort(403)
    form = PlayForm()
    use=username
    question = current_user.question
    user = User.query.get(current_user.id)
    user_collection = mongo.db.Questions
    s = user_collection.find_one({'question_number':user.question})
    answers = form.answer.data
    if form.validate_on_submit:
        if answers is not None:
            log = Logs(answer = answers.lower(),answer_time = datetime.now(),question = user.question,userid = current_user.id)
            db.session.add(log)
            db.session.commit()
            if answers.lower() == s['q_answer']:
                user.question += 1
                user.answer_time= datetime.now()
                db.session.add(user)
                db.session.commit()
                return render_template('Correct.html')
            return render_template('Wrong.html')
    return render_template('play.html',form=form,use=use,question=s['question'])

@app.route('/leaderboard')
@login_required
def leaderboard():
    all_users = User.query.order_by(User.question.desc(),User.answer_time.asc()).all()
    n = len(all_users)
    print(n)
    rank = []
    for users in all_users:
        rank.append(n)
        n -= 1
    return render_template('leaderboard.html',all_users=all_users,rank=rank)

@app.route('/admin_panel',methods=['GET','POST'])
@login_required
def admin():
    if current_user.username != 'Xino':
        abort(403)
    else:
        all_logs = Logs.query.order_by(Logs.answer_time.desc())
        return render_template("admin_panel.htm",all_logs=all_logs)

@app.route('/profile/<user_id>',methods = ['GET','POST'])
@login_required
def profile(user_id):
    if current_user.username != 'Xino':
        abort(403)
    user = User.query.get(user_id)
    logs = []
    if user.logs:
        for i in user.logs:
            logs.append(i)
    return render_template("profile.htm",user=user,logs=logs)

@app.route('/restrict/<username>',methods = ['GET','POST'])
@login_required
def ban(username):
    if current_user.username != 'Xino':
        abort(403)
    all = User.query.filter_by(username = username)
    if all:
        all[0].restricted = "Yes"
        db.session.commit()
        return redirect(url_for('admin'))
    return abort(404)

@app.route('/unrestrict/<username>',methods = ['GET','POST'])
@login_required
def unban(username):
    if current_user.username != 'Xino':
        abort(403)
    all = User.query.filter_by(username = username)
    if all:
        all[0].restricted = "No"
        db.session.commit()
        return redirect(url_for('admin'))
    return abort(404)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error_404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
