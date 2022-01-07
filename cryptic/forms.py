from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo, ValidationError,Length

from cryptic import app,db
from cryptic.models import User
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired()])
    lname = StringField('Last Name')
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    classe = StringField('Class', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match'), Length(min = 8, max=16)])
    pass_confirm = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email you chose has already been registered')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username you chose has already been registered')
        if " " in field.data or "'" in field.data or '"' in field.data:
            raise ValidationError('No spaces or specialchars in username')

class PlayForm(FlaskForm):
    answer = StringField(label='solve the question',validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_answer(self,field):
        if " " in field.data or "'" in field.data or '"' in field.data:
            raise ValidationError('No spaces or specialchars in answer')
