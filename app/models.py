from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json

from . import db, login

with open('app/multipliers.json', 'r') as file:
    multipliers = json.load(file)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


responsibilities = db.Table('responsibilities',
                            db.Column('teacher_id', db.Integer,
                                      db.ForeignKey('teacher.id'),
                                      primary_key=True),
                            db.Column('resp_id', db.Integer,
                                      db.ForeignKey('responsibility.id'),
                                      primary_key=True)
                            )


instructors = db.Table('instructors',
                       db.Column('teacher_id', db.Integer,
                                 db.ForeignKey('teacher.id'),
                                 primary_key=True),
                       db.Column('course_id', db.Integer,
                                 db.ForeignKey('course.id'),
                                 primary_key=True))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    grades = db.Column(db.Boolean)
    hs = db.Column(db.Boolean)
    courses = db.relationship('Course', backref='teacher', lazy='dynamic')
    courselist = db.relationship('Course',
                                 secondary=instructors,
                                 primaryjoin=(instructors.c.teacher_id == id),
                                 backref=db.backref('instructor',
                                                    lazy='dynamic'),
                                 lazy='dynamic')
    responsibilities = db.relationship('Responsibility',
                                       secondary=responsibilities,
                                       primaryjoin=(
                                           responsibilities.c.teacher_id == id),
                                       backref=db.backref('member',
                                                          lazy='dynamic'),
                                       lazy='dynamic')

    def __repr__(self):
        return '<Teacher {} {}>'.format(self.first_name, self.last_name)

    def teaching_load(self):
        return int(sum([course.total_time() for course in self.courses]))

    def teaching_load_p(self):
        return int(100 * self.teaching_load() /
                   (multipliers['weeks/year'] * 20 * 45))

    def nt_load(self):
        return int(sum([resp.total_time() for resp in
                        self.responsibilities]))

    def total_load(self):
        return self.teaching_load() + self.nt_load()

    def total_load_p(self):
        return int(100 * self.total_load() /
                   (multipliers['FT Expectation']))


# todo adjust model to make more than one instructor possible

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.String(64))
    weeks = db.Column(db.Float)
    min_per_week = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teachers = db.relationship('Teacher', secondary=instructors,
                               primaryjoin=(instructors.c.course_id == id),
                               backref=db.backref('course',
                                                  lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.title)

    def total_time(self):
        if self.weeks and self.min_per_week:
            return int(self.weeks * self.min_per_week * multipliers[self.type])
        else:
            return 0


class Responsibility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    hours_per_month = db.Column(db.Float)
    months_per_year = db.Column(db.Float)
    members = db.relationship('Teacher', secondary=responsibilities,
                              primaryjoin=(responsibilities.c.resp_id == id),
                              backref=db.backref('responsibility',
                                                 lazy='dynamic'),
                              lazy='dynamic')

    def __repr__(self):
        return '<Responsibility {}>'.format(self.name)

    def total_time(self):
        if self.hours_per_month and self.months_per_year:
            return 60 * self.hours_per_month * self.months_per_year * multipliers['Other']
        else:
            return 0
