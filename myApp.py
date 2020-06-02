from flask import Flask, render_template, request
from forms import registration_form


app = Flask(__name__)  # '__main__'


@app.route('/')
def home():
    return render_template("HomePage.html")

@app.route('/Register')
def register():
    return render_template("Register.html")

@app.route('/Login')
def login():
    return render_template("Login.html")



@app.route('/logged_in')
def login_popup():
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template("login_popup.html", username=username, password=password)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
