from cryptic import app,db
from flask import render_template,redirect,url_for,request,flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from cryptic.models import User,Logs,Questions
from cryptic.forms import LoginForm,RegistrationForm,PlayForm
from sqlalchemy import desc , asc
from werkzeug.security import generate_password_hash,check_password_hash
username =''
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
@app.route('/')
def home():
    # question=Questions(question = "kya yuvaan nalla hai",
    #         answer = "yes",
    #         source = "do u hv to think",
    # )
    # db.session.add(question)
    # db.session.commit()
    # db.session.commit()
    return render_template('HomePage.html')

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
                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('home')
                return redirect(next)
            else:
                mess = "Wrong Password"
        except AttributeError:
            mess = 'No such login.Pls register to make an account '
    print(mess)
    return render_template('Login.html', form=form,mess=mess)

@app.route('/register',methods=['GET','POST'])
def register():
    mess = 'Register to play the most exciting cryptic hunts ever'
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
    return render_template('Register.html',form = form,mess=mess)
@app.route('/play',methods=['GET','POST'])
@login_required
def play():
    if current_user.restricted=="Yes":
        abort(403)
    form = PlayForm()
    mess = ""
    max = Questions.query.order_by(Questions.id.desc())
    for i in max:
        print(i.id)
    print(max)
    questions = current_user.question
    user = User.query.get(current_user.id)
    if user.question > max[0].id:
        return "Congratulations and celeberations! Admins gonna contact"
    question = Questions.query.get(user.question)
    answers = form.answer.data
    if form.validate_on_submit():
        if answers is not None:
            log = Logs(answer = answers.lower(),answer_time = datetime.now(),question = user.question,userid = current_user.id)
            db.session.add(log)
            db.session.commit()
            if answers.lower() == question.answer:
                user.question += 1
                user.answer_time= datetime.now()
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('play'))
            else:
                mess = "wrong"
    return render_template('play.html',form=form,use=questions,question=question.question,mess=mess,source = question.source,imgur = question.imgur)

@app.route('/leaderboard')
@login_required
def leaderboard():
    all_users = User.query.order_by(User.question.desc(),User.answer_time.asc()).all()
    rank = []
    all = []
    l = 0
    for users in all_users:
        if users.restricted == "Yes" or users.username == "Xino":
            pass
        else:
            all.append(users)
    n = len(all)
    for i in all:
        rank.append(n)
        n -= 1
    return render_template('leaderboard.html',all_users=all,rank=rank)

@app.route('/admin_panel',methods=['GET','POST'])
@login_required
def admin():
    if current_user.username != 'Xino':
        abort(403)
    else:
        all_logs = Logs.query.order_by(Logs.answer_time.desc())
        return render_template("admin_panel.htm",all_logs=all_logs)

@app.route('/profile/<username>',methods = ['GET','POST'])
@login_required
def profile(username):
    if current_user.username != 'Xino':
        abort(403)
    user = User.query.filter_by(username=username)
    logs = []
    if user:
        if user[0].logs:
            for i in user[0].logs:
                logs.append(i)
    return render_template("profile.htm",user=user[0],logs=logs)

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
