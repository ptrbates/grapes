#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User, Teacher, Course, Responsibility
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_teacher_course(self):
        t = Teacher(last_name='brown')
        c = Course(title='course 1')
        db.session.add(t)
        db.session.add(c)
        db.session.commit()
        c.teacher_id = t.id
        self.assertTrue(c in t.courses)

    def test_teacher_resp(self):
        t = Teacher(last_name='brown')
        r = Responsibility(name='resp 1')
        r.members.append(t)
        self.assertTrue(r in t.responsibilities)
        self.assertTrue(t in r.members)


if __name__ == '__main__':
    unittest.main(verbosity=2)