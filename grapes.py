from app import create_app, db
from app.models import User, Teacher, Course, Responsibility
from app.main.course_conversion import course_conversion

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Teacher': Teacher,
            'Course': Course, 'Responsibility': Responsibility,
            'cc': course_conversion}
