# This script moves courses listed under Teacher.courses to Teacher.courselist

from .. import db
from ..models import Course, Teacher


def course_conversion():
    courses = Course.query.all()
    for course in courses:
        print(course.title)
        t = Teacher.query.filter_by(id=course.teacher_id).first()
        if t not in course.teachers.all():
            course.teachers.append(t)
            db.session.add(course)
            db.session.commit()
