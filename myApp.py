from cryptic import app,db
from flask import render_template,redirect,url_for,request,flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from cryptic.models import User
from cryptic.forms import LoginForm,RegistrationForm,PlayForm
from werkzeug.security import generate_password_hash,check_password_hash

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
    form = RegistrationForm()
    email = form.email.data
    username = form.username.data
    password = form.password.data
    fname = form.fname.data
    lname = form.lname.data

    if form.validate_on_submit():
        user = User(email,username,password,1,fname,lname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('Register.html',form = form)
@app.route('/play',methods=['GET','POST'])
def play():
    form = PlayForm()
    question = current_user.question
    user = User.query.get(current_user.id)
    answer = form.answer.data
    if question == 1:
        if form.validate_on_submit:
            if answer is not None:
                if answer.lower() == 'lo':
                    user.question += 1
                    db.session.add(user)
                    db.session.commit()
                    return render_template('Correct.html')
    return render_template('play.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
