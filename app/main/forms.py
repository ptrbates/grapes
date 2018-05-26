from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app.models import multipliers


class AddTeacherForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name', validators=[DataRequired()])
    grades = BooleanField('Teaches in the grades?')
    hs = BooleanField('Teacher in the high school?')
    submit = SubmitField('Add Teacher')


class AddCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    type = SelectField('Course Type', choices=[('Arts/Movement', 'Arts/Movement'),
                                               ('Foreign Language', 'Foreign Language'),
                                               ('Grades Main Lesson', 'Grades Main Lesson'),
                                               ('Grades Specialty', 'Grades Specialty'),
                                               ('Humanities/Chemistry', 'Humanities/Chemistry'),
                                               ('Other', 'Other'),
                                               ('Recess/Lunch', 'Recess/Lunch'),
                                               ('STEM', 'STEM')],
                       validators=[DataRequired()])
    teacher_id = SelectField('Instructor', coerce=int)
    weeks = FloatField('Course Duration (weeks)', validators=[DataRequired()])
    min_per_week = IntegerField('Minutes per week', validators=[DataRequired()])
    submit = SubmitField('Add Course')


class AddResponsibilityForm(FlaskForm):
    name = StringField('Name of Responsibility', validators=[DataRequired()])
    hours_per_month = FloatField('Hours per Month', validators=[DataRequired()])
    months_per_year = FloatField('Months per Year', validators=[DataRequired()])
    submit = SubmitField('Add Responsibility')


class ChangeTeacherForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    grades = BooleanField('Teaches in the grades?')
    hs = BooleanField('Teacher in the high school?')
    change = SubmitField('Make Changes')
    delete = SubmitField('Delete Teacher')


class ChangeCourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    type = SelectField('Course Type', choices=[('Grades Main Lesson', 'Grades Main Lesson'),
                                               ('Recess/Lunch', 'Recess/Lunch'),
                                               ('Arts/Movement', 'Arts/Movement'),
                                               ('Foreign Language', 'Foreign Language'),
                                               ('STEM', 'STEM'),
                                               ('Humanities/Chemistry', 'Humanities/Chemistry'),
                                               ('Grades Specialty', 'Grades Specialty'),
                                               ('Other', 'Other')],
                       validators=[DataRequired()])
    teacher_id = SelectField('Instructor', coerce=int)
    weeks = FloatField('Course Duration (weeks)', validators=[DataRequired()])
    min_per_week = IntegerField('Minutes per week', validators=[DataRequired()])
    assign = SubmitField('Make Changes')
    delete = SubmitField('Delete Course')


class ChangeResponsibilityForm(FlaskForm):
    name = StringField('Name of Responsibility', validators=[DataRequired()])
    hours_per_month = FloatField('Hours per Month', validators=[DataRequired()])
    months_per_year = FloatField('Months per Year', validators=[DataRequired()])
    change = SubmitField('Update Responsibility')
    delete = SubmitField('Delete Responsibility')


class AssignCourseForm(FlaskForm):
    course_id = SelectField('Assign Courses:', coerce=int)
    assign = SubmitField('Assign Course')
    remove = SubmitField('Remove Course')


class AssignResponsibilityForm(FlaskForm):
    resp_id = SelectField('Assign Responsibilities:', coerce=int)
    assign = SubmitField('Assign Responsibility')
    remove = SubmitField('Remove Responsibility')


class AssignMemberForm(FlaskForm):
    teacher_id = SelectField('Choose Teacher:', coerce=int)
    assign = SubmitField('Assign Teacher')
    remove = SubmitField('Remove Teacher')


class ChooseViewForm(FlaskForm):
    view_all = SubmitField('View All')
    view_hs = SubmitField('View HS Only')
    view_grades = SubmitField('View Grades Only')


class ChangeMultipliersForm(FlaskForm):
    grades_ML = FloatField('Grades ML', default=multipliers['Grades Main Lesson'])
    weekspyear = IntegerField('Weeks/year', default=multipliers['weeks/year'])
    ft_exp = IntegerField('FT Expectation', default=multipliers['FT Expectation'])
    recess = FloatField('Recess/Lunch', default=multipliers['Recess/Lunch'])
    arts_movement = FloatField('Arts/Movement', default=multipliers['Arts/Movement'])
    fl = FloatField('Foreign Language', default=multipliers['Foreign Language'])
    stem = FloatField('STEM', default=multipliers['STEM'])
    humchem = FloatField('Humanities/Chemistry', default=multipliers['Humanities/Chemistry'])
    grades_spec = FloatField('Grades Specialty', default=multipliers['Grades Specialty'])
    other = FloatField('Other', default=multipliers['Other'])
    submit = SubmitField('Submit Changes')

