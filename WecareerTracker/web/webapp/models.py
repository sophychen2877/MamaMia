from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, migrate
from sqlalchemy.orm.attributes import QueryableAttribute
from flask import json
from datetime import datetime as dt

class User(db.Model, UserMixin):

    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':role
    }

    def __init__(self,username,email):
        self.username = username
        self.email = email

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.role == 'admin':
            return password == self.password_hash
        return check_password_hash(self.password_hash, password)

    def is_mentor(self):
        return False

    def is_admin(self):
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity':'admin'
    }
    def is_admin(self):
        return True

class Mentor(User):
    __tablename__ = 'mentor'
    id = db.Column(db.Integer,primary_key=True)
    user_mentor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(64),index=True)
    __mapper_args__ = {
        'polymorphic_identity':'mentor'
    }
    def is_mentor(self):
        return True
    def set_name(self, name):
        self.name = name


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer,primary_key=True)
    user_student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(64),index=True)
    skills = db.Column(db.String(128))
    __mapper_args__ = {
        'polymorphic_identity':'student'
    }
    def set_name(self, name):
        self.name = name

    applications = db.relationship('Application', backref="student", lazy=True)


class Mentorship(db.Model):
    __tablename__ = 'mentorship'
    id = db.Column(db.Integer, primary_key=True,index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'),nullable=False)
    active_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)

    def __init__(self, student_id,mentor_id):
        self.student_id = student_id
        self.mentor_id = mentor_id

    def set_end_date(self):
        self.end_date = dt.now()

    def set_active_date(self,date):
        self.active_date = date


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Application(db.Model):
    __tablename__ = 'application'
    # __searchable__ = ['company', 'title']
    application_id = db.Column(db.Integer,primary_key=True, index=True)
    company = db.Column(db.String(100),index=True)
    title = db.Column(db.String(100),index=True)
    link = db.Column(db.String(100))
    entry_time = db.Column(db.DateTime, index=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)

    actions= db.relationship('Action', backref="application", cascade="all,delete", lazy=True)
    notes = db.relationship('MentorNote', backref="application", cascade="all,delete", lazy=True)

    def set_time(self):
        self.entry_time = dt.now()

    def delete_application(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Action(db.Model):

    __tablename__ = 'action'
    action_id = db.Column(db.Integer, primary_key=True)
    application_version = db.Column(db.Integer, index=True)
    status = db.Column(db.String(20), index=True)
    date = db.Column(db.Date, index=True)
    comment = db.Column(db.String(200), index=True)
    entry_time = db.Column(db.DateTime, index=True)

    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'),nullable=False)

    def set_time(self):
        self.entry_time = dt.now()

    def set_version(self,version):
        self.application_version = version

class MentorNote(db.Model):
    __tablename__ = 'mentor_note'
    note_id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(1000))
    entry_time = db.Column(db.DateTime, index=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'),nullable=False)

    def set_time(self):
        self.entry_time = dt.now()







# class Appointment(db.Model):
#     __tablename__ = 'appointment'
#     appointment_id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
#     mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'),nullable=False)
#     datetime = db.Column(db.DateTime, index=True)
#     confirm = db.Column(db.Boolean)
#
#
#     def __init__(self, student_id,mentor_id):
#         self.student_id = student_id
#         self.mentor_id = mentor_id
#         self.confirm = False
#
#     def set_date(self,datetime):
#         self.datetime = datetime
#
#     def set_confirm(self):
#         self.confirm = True
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
