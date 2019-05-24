from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms import validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User
import wtforms
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])#, Email()
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

#form to add application which only has fields for company, title, and application link
class ApplicationForm(FlaskForm):
    company = StringField('Company name', validators=[DataRequired()])
    title = StringField('Job Title', validators=[DataRequired()])
    link = StringField('Web Link', [validators.optional()])

#form to change the application which has fields for date, status, and student comment
class ActionForm(FlaskForm):
    date = DateField('Action Date', validators=[DataRequired()], format='%Y-%m-%d')
    status = SelectField('Progress Status', choices=[('1','Checked'),('2','Applied') ,('3','Received 1st round interview'),('4','Received 2nd round interview') ,('5','Received offer') ])
    comment = TextAreaField('Comment', [validators.optional(), validators.length(max=200)])
    save = SubmitField()

#a combined form for application + action
class CombineForm(FlaskForm):
    app_form = wtforms.FormField(ApplicationForm)
    act_form = wtforms.FormField(ActionForm)
    submit = SubmitField()

#appoinment form
# class AppointmentForm(FlaskForm):
#     date = DateTimeField('Appointment Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
#     comment = TextAreaField('Comment', [validators.optional(), validators.length(max=200)])
#     confirm = SubmitField()


#form for mentor to log time
# class LogTimeForm(FlaskForm):
#     start_time = DateTimeField('Start Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
#     end_time = DateTimeField('End Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
