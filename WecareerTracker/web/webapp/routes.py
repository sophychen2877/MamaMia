from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user,current_user,login_required
from werkzeug.urls import url_parse
from .models import User, Application, Action, Mentor,Student, Mentorship,MentorNote
from .forms import LoginForm, RegistrationForm, CombineForm, ActionForm
from datetime import datetime as dt
from flask import current_app as app
from functools import wraps
import json
from .import db
from sqlalchemy import func
from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

app.session_interface = CustomSessionInterface()

# @user_loaded_from_header.connect
# def user_loaded_from_header(self, user=None):
#     g.login_via_header = True


statuses={'1':'Checked', '2':'Applied','3':'Received 1st round interview','4':'Received 2nd round interview','5':'Received offer'}

#user_loader function from login_manager (this is a required function for flask-login)
@app.login_manager.user_loader
def load_user(id):
    return User.query.get(id)

#login_required decorator_function
def login_required(user_role='user'):
    def decorator_function(fn):
        @wraps(fn)
        def wrapper_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return app.login_manager.unauthorized()
            this_role = current_user.role
            if (this_role != user_role) and (user_role != 'user') and (user_role != 'admin'):
                return app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return wrapper_function
    return decorator_function

#home page for not registered/not logged in users
@app.route('/')
@app.route('/index')
def front_page():
    return render_template('base.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        student.set_password(form.password.data)
        student.set_name(form.name.data)
        student.save_to_db()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#log-in page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is None) or ((not user.check_password(form.password.data)) and (not user.is_admin())):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        flash('Logged in successfully.')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.is_mentor():
                next_page = url_for('mentor_dashboard')
            elif user.is_admin():
                next_page = url_for('mentorship')
            else:
                next_page = url_for('student_dahsboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#user logging out then is redirected to homepage
@app.route('/logout')
@login_required(user_role='user')
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('front_page'))


#student's view only - student home page when they just logged in which shows their current application progress & dashboard
@app.route('/home')
@login_required(user_role='student')
def student_dahsboard():
    student_id = current_user.id
    mentorship = Mentorship.query.filter_by(student_id=student_id).first()
    if not mentorship:
        flash('you don\'t have a mentor yet')
        mentor_name = None
    else:
        mentor_name = Mentor.query.filter_by(id=mentorship.mentor_id).first().name

    applications = Application.query.filter_by(student_id=student_id).order_by(Application.application_id).all()

    application_list = [{'id': i.application_id, 'company': i.company, 'title':i.title, 'link':i.link, \
    'note':MentorNote.query.filter_by(application_id=i.application_id).order_by(MentorNote.entry_time.desc()).first(),\
    'status': statuses[Action.query.filter_by(application_id=i.application_id).order_by(Action.application_version.desc()).limit(1).first().status]}\
     for i in applications]
    #TO-DO's

    #no.of applications Applied
    application_applied = Application.query.filter_by(student_id=student_id).count()
    #no.of interviews received

    #last
    return render_template('applications.html', title='application list',application=application_list,mentor_name=mentor_name)

#student's view only - student has the ability to add applications
@app.route('/applications/add', methods=['GET','POST'])
@login_required(user_role='student')
def add_application():
    form = CombineForm()
    if form.validate_on_submit():
        user = current_user
        application = Application(company=form.app_form.company.data, title=form.app_form.title.data, link=form.app_form.link.data, student=user)
        action = Action(status=form.act_form.status.data, date=form.act_form.date.data, comment=form.act_form.comment.data)
        action.set_version(1)
        application.set_time()
        action.set_time()
        user.applications.append(application)
        application.actions.append(action)
        user.save_to_db()
        flash(f'Created application successful')
        return redirect(url_for('student_dahsboard'))
    return render_template('add_application.html',title='Add a new application',form=form)

#student's view only - student has the ability to edit on their application (change status, add comments etc)
@app.route('/applications/<int:id>', methods=['GET','POST'])
@login_required(user_role='student')
def edit_application(id):
    user = current_user
    application = Application.query.filter_by(application_id=id).first()
    application_dict = {'id': application.application_id,'company': application.company, 'title': application.title, 'link': application.link}
    action_list = Action.query.filter_by(application_id=id).order_by(Action.action_id).all()
    action_dict = [{'id': i.application_version, 'status': statuses[i.status], 'date':i.date, 'comment':i.comment} for i in action_list]
    comments = MentorNote.query.filter_by(application_id=id).order_by(MentorNote.entry_time.desc()).all()
    form = ActionForm()
    if form.validate_on_submit():
        action = Action(status=form.status.data, date=form.date.data,comment=form.comment.data)
        action.set_time()
        version = Action.query.filter_by(application_id=application.application_id).count()
        action.set_version(version+1)
        application.actions.append(action)
        application.save_to_db()
        flash(f'Edited appilication successful')
        return redirect(url_for('student_dahsboard'))
    return render_template('edit_application.html',title='change application status',application=application_dict, form=form, actions=action_dict, comments=comments)


#student's view only (+admin) - student can delete their applcations on their application dashboard then gets redirect for the student home page
@app.route('/delete_application/<int:id>', methods=['POST'])
@login_required(user_role='student')
def delete_application(id):
    application = Application.query.filter_by(application_id=id).first()
    application.delete_application()
    flash(f'Appilication deleted successful')
    return redirect(url_for('student_dahsboard'))


#mentor's view only (+admin) - mentor the last 5 applications of their matching student,
@app.route('/dashboard',methods=['GET'])
@login_required(user_role='mentor')
def mentor_dashboard():
    mentor = current_user
    mentorship_list = Mentorship.query.filter_by(mentor_id=mentor.id).all()
    student_id_list = [l.student_id for l in mentorship_list]
    matching_student = [Student.query.filter_by(id=i).first() for i in student_id_list]
    matching_applications = [Application.query.filter_by(student_id=i).limit(5).all() for i in student_id_list]
    return render_template('mentor_dashboard.html', title='dashboard',students=matching_student, applications=matching_applications[0])

@app.route('/dashboard/<int:id>', methods=['GET','POST'])
@login_required(user_role='mentor')
def student_detail(id):
    mentor = current_user
    student = Student.query.filter_by(id=id).first()
    applications = Application.query.filter_by(student_id=id).all()
    latest_actions = [{'application': Application.query.filter_by(application_id=app.application_id).first(), 'action': Action.query.filter_by(application_id=app.application_id).order_by(Action.application_version.desc()).limit(1).all()} for app in applications]
    return render_template('student_applications.html', title='applications', student=student, list=latest_actions, status=statuses)


@app.route('/dashboard/applications/<int:id>', methods=['GET','POST'])
@login_required(user_role='mentor')
def application_detail(id):
    application = Application.query.filter_by(application_id=id).first()
    student_id = application.student_id
    actions = Action.query.filter_by(application_id=id).order_by(Action.application_version.desc()).all()
    comments = MentorNote.query.filter_by(application_id=id).order_by(MentorNote.entry_time.desc()).all()
    if request.method == 'POST':
        comment = request.form.get('comment')
        note = MentorNote(note=comment, application_id=id)
        note.set_time()
        application.notes.append(note)
        application.save_to_db()
        return redirect(url_for('application_detail', id=id))
    return render_template('application_details.html', title='application', application=application,list=actions, student_id=student_id, status=statuses, comment=comments)

#admin's view only - admin can match mentorship between student + mentor
@app.route('/mentorship', methods=['GET','POST'])
@login_required(user_role='admin')
def mentorship():
    students = Student.query.all()
    mentors = Mentor.query.all()
    mentorship = Mentorship.query.filter_by(end_date=None).all()
    mentorship_dict = [{'id':m.id,'mentor_name':Mentor.query.filter_by(id=m.mentor_id).first().name,'student_name':Student.query.filter_by(id=m.student_id).first().name, 'date':m.active_date} for m in mentorship]
    if request.method == 'POST':
        mentor_id = request.form.get('mentor')
        student_id = request.form.get('student')
        mentorship = Mentorship(student_id=student_id, mentor_id=mentor_id)
        mentorship.set_active_date(request.form.get('mentorship_start'))
        mentorship.save_to_db()
        return redirect(url_for('mentorship'))
    return render_template('admin_mentorship.html', students=students, mentors=mentors, mentorship=mentorship_dict)

@app.route('/end_mentorship/<int:id>', methods=['POST'])
@login_required(user_role='admin')
def end_mentorship(id):
    mentorship = Mentorship.query.filter_by(id=id).first()
    mentorship.set_end_date()
    mentorship.save_to_db()
    flash(f'Mentorship ended')
    return redirect(url_for('mentorship'))


#admin's view only - admin can create mentor accounts
@app.route('/mentor_register', methods=['GET','POST'])
@login_required(user_role='admin')
def mentor_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        mentor = Mentor(username=form.username.data, email=form.email.data)
        mentor.set_password(form.password.data)
        mentor.set_name(form.name.data)
        mentor.save_to_db()
        flash('Congratulations, you just registered a mentor!')
        return redirect(url_for('mentorship'))
    return render_template('register.html', title='Registration for Mentors',form=form)


# add appointmnt
# @app.route('/appointment/add',methods=['GET','POST'])
# @login_required(user_role='student')
# def add_appointment():
#     mentor = Mentorship.query.filter_by(student_id=current_user.id).first()
#     form = AppointmentForm()
#     if form.validate_on_submit():
#
#     return render_template('add_appointment.html',title='Add a new appointment',form=form)

# @app.route('/appointment/confirm', methods=['GET','POST'])
# @login_required(user_role='mentor')
# def confirm_appointment():
