#!/usr/bin/env python
import unittest
from .. import create_app, db, mail
from ..models import User, Teacher, Course, Responsibility
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    DEBUG = False


# todo Expand tests to include dropping responsibilities, courses, teachers

class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        mail.init_app(self.app)
        self.assertEqual(self.app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_app(self):
        app = create_app(TestConfig)
        return app


class UserModelCase(TestBase):
    def test_user_insert(self):
        u = User(username='susan')
        db.session.add(u)
        db.session.commit()
        assert u in db.session

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))


class TeacherModelCase(TestBase):
    def test_teacher_course(self):
        t = Teacher(last_name='brown')
        c = Course(title='course1')
        db.session.add(t)
        db.session.add(c)
        db.session.commit()
        c.teacher_id = t.id
        self.assertTrue(c in t.courses)
        self.assertTrue(c.teacher == t)

    def test_teacher_resp(self):
        t = Teacher(last_name='brown')
        t2 = Teacher(last_name='smith')
        db.session.add(t, t2)
        r = Responsibility(name='resp1')
        r2 = Responsibility(name='resp2')
        r.members.append(t)
        r.members.append(t2)
        r2.members.append(t)
        db.session.add(r, r2)
        db.session.commit()
        assert t, t2 in r.members
        assert t in r2.members
        assert r, r2 in t.responsibilities
        assert r in t2.responsibilities


if __name__ == '__main__':
    unittest.main(verbosity=2)
