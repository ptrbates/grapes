from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.main.forms import AddTeacherForm, AddCourseForm, AddResponsibilityForm, AssignMemberForm,  \
    AssignCourseForm, ChangeCourseForm, ChangeTeacherForm, ChangeResponsibilityForm, \
    ChangeMultipliersForm, ChooseViewForm
from app.models import Teacher, Course, Responsibility
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/teacher_list', methods=['GET', 'POST'])
@login_required
def teacher_list():
    title = 'Teacher Load Summary'
    teachers = Teacher.query.order_by('last_name').all()
    form = ChooseViewForm()
    if form.validate_on_submit():
        if form.view_hs.data:
            teachers = Teacher.query.filter_by(hs=True).order_by('last_name').all()
            title = 'High School Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_grades.data:
            teachers = Teacher.query.filter_by(grades=True).order_by('last_name').all()
            title = 'Grades Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        else:
            teachers = Teacher.query.order_by('last_name').all()
            title = 'Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)

    return render_template('teacher_list.html', title=title, teachers=teachers, form=form)


@bp.route('/teacher_view/<tid>', methods=['GET', 'POST'])
@login_required
def teacher_view(tid):
    teacher = Teacher.query.filter_by(id=tid).first()
    title = 'Teacher View: {} {}'.format(teacher.first_name, teacher.last_name)

    form_a = AssignCourseForm()
    form_a.course_id.choices = [(c.id, c.title) for c in Course.query.order_by('title')]
    if form_a.validate_on_submit():
        course_id = form_a.course_id.data
        course = Course.query.filter_by(id=course_id).first()
        course.teacher_id = teacher.id
        db.session.add(teacher)
        db.session.commit()
        flash('Course assigned.')
        return redirect(url_for('main.teacher_view', tid=teacher.id))

    form_c = ChangeTeacherForm()
    form_c.first_name.data = teacher.first_name
    form_c.last_name.data = teacher.last_name
    form_c.grades.data = teacher.grades
    form_c.hs.data = teacher.hs
    if form_c.validate_on_submit():
        if form_c.change.data:
            teacher.first_name = form_c.first_name.data
            teacher.last_name = form_c.last_name.data
            teacher.grades = form_c.grades.data
            teacher.hs = form_c.hs.data
            db.session.add(teacher)
            db.session.commit()
            flash('Updates applied.')
            return redirect(url_for('main.teacher_view', tid=teacher.id))
        if form_c.delete.data:
            db.session.delete(teacher)
            db.session.commit()
            flash('Teacher removed from database.')
            return redirect(url_for('main.teacher_list'))

    return render_template('teacher_view.html', teacher=teacher, courses=teacher.courses,
                           resps=teacher.responsibilities, title=title, form_a=form_a, form_c=form_c)


@bp.route('/course_list', methods=['GET', 'POST'])
@login_required
def course_list():
    courses = Course.query.order_by('title').all()

    return render_template('course_list.html', title='Course List', courses=courses)


@bp.route('/course_view/<cid>', methods=['GET', 'POST'])
@login_required
def course_view(cid):
    course = Course.query.filter_by(id=cid).first()
    title = 'Course View: {}'.format(course.title)

    form = ChangeCourseForm()
    form.title.data = course.title
    form.type.data = course.type
    form.weeks.data = course.weeks
    form.min_per_week.data = course.min_per_week
    form.teacher_id.choices = [(t.id, t.last_name + ' ' + t.first_name) for t in Teacher.query.order_by('last_name')]
    if form.validate_on_submit():
        if form.assign.data:
            course.title = form.title.data
            course.type = form.type.data
            course.weeks = form.weeks.data
            course.min_per_week = form.min_per_week.data
            course.teacher_id = form.teacher_id.data
            db.session.add(course)
            db.session.commit()
            flash('Updates applied.')
            return redirect(url_for('main.course_list'))
        elif form.delete.data:
            db.session.delete(course)
            db.session.commit()
            flash('Course removed from database.')
            return redirect(url_for('main.course_list'))

    return render_template('course_view.html', course=course, title=title, form=form)


@bp.route('/responsibility_list', methods=['GET', 'POST'])
@login_required
def responsibility_list():
    resps = Responsibility.query.order_by('name').all()

    return render_template('responsibility_list.html', title='Responsibility List', resps=resps)


@bp.route('/responsibility_view/<rid>', methods=['GET', 'POST'])
@login_required
def responsibility_view(rid):
    resp = Responsibility.query.filter_by(id=rid).first()
    title = 'Responsibility View: {}'.format(resp.name)

    form_a = AssignMemberForm()
    form_a.teacher_id.choices = [(t.id, t.last_name + ' ' + t.first_name) for t in Teacher.query.order_by('last_name')]
    if form_a.validate_on_submit():
        teacher = Teacher.query.filter_by(id=form_a.teacher_id.data).first()
        resp.members.append(teacher)
        db.session.add(resp)
        db.session.commit()
        return redirect(url_for('main.responsibility_list'))

    form_c = ChangeResponsibilityForm()
    form_c.name.data = resp.name
    form_c.months_per_year.data = resp.months_per_year
    form_c.hours_per_month.data = resp.hours_per_month
    if form_c.validate_on_submit():
        if form_c.change.data:
            resp.name = form_c.name.data
            resp.hours_per_month = form_c.hours_per_month.data
            resp.months_per_year = form_c.months_per_year.data
            db.session.add(resp)
            db.session.commit()
            flash('Updates applied.')
            return redirect(url_for('main.responsibility_view', rid=resp.id))
        elif form_c.delete.data:
            db.session.delete(resp)
            db.session.commit()
            flash('Responsibility removed from database.')
            return redirect(url_for('main.responsibility_list'))

    return render_template('responsibility_view.html', resp=resp, title=title, form_a=form_a, form_c=form_c)


@bp.route('/adds', methods=['GET', 'POST'])
@login_required
def adds():
    title = 'Add Items'
    t_form = AddTeacherForm()
    if t_form.validate_on_submit():
        teacher = Teacher(first_name=t_form.first_name.data, last_name=t_form.last_name.data,
                          grades=t_form.grades.data, hs=t_form.hs.data)
        db.session.add(teacher)
        db.session.commit()
        flash('{} {} added to teacher list.'.format(teacher.first_name, teacher.last_name))
        return redirect(url_for('main.adds'))

    r_form = AddResponsibilityForm()
    if r_form.validate_on_submit():
        resp = Responsibility(name=r_form.name.data, hours_per_month=r_form.hours_per_month.data,
                              months_per_year=r_form.months_per_year.data)
        db.session.add(resp)
        db.session.commit()
        flash('{} added to responsibilities list.'.format(resp.name))
        return redirect(url_for('main.adds'))

    c_form = AddCourseForm()
    c_form.teacher_id.choices = [(0, "---")] + [(t.id, t.last_name + ", " + t.first_name)
                                                for t in Teacher.query.order_by('last_name')]
    if c_form.validate_on_submit():
        if c_form.teacher_id.data != '':
            course = Course(title=c_form.title.data, type=c_form.type.data, weeks=c_form.weeks.data,
                            min_per_week=c_form.min_per_week.data, teacher_id=c_form.teacher_id.data)
        else:
            course = Course(title=c_form.title.data, type=c_form.type.data, weeks=c_form.weeks.data,
                            min_per_week=c_form.min_per_week.data)
        db.session.add(course)
        db.session.commit()
        flash('{} added to course list.'.format(course.title))
        return redirect(url_for('main.adds'))

    return render_template('adds.html', title=title, t_form=t_form, r_form=r_form, c_form=c_form)


@bp.route('/multipliers', methods=['GET', 'POST'])
@login_required
def change_multipliers():
    form = ChangeMultipliersForm()
    title = 'Change Multipliers'
    if form.validate_on_submit():
        multipliers['Grades Main Lesson'] = form.grades_ML.data
        multipliers['weeks/year'] = form.weekspyear.data
        multipliers['FT Expectation'] = form.ft_exp.data
        multipliers['Recess/Lunch'] = form.recess.data
        multipliers['Arts/Movement'] = form.arts_movement.data
        multipliers['Foreign Language'] = form.fl.data
        multipliers['STEM'] = form.stem.data
        multipliers['Humanities/Chemistry'] = form.humchem.data
        multipliers['Grades Specialty'] = form.humchem.data
        multipliers['Other'] = form.other.data
        flash('Multipliers updated successfully.')

    return render_template('change_multipliers.html', title=title, form=form)


multipliers = {'Grades Main Lesson': 20 / 20,
               'weeks/year': 35,
               'FT Expectation': 39000,
               'Recess/Lunch': 20 / 20,
               'Arts/Movement': 20 / 20,
               'Foreign Language': 20 / 19,
               'STEM': 20 / 18,
               'Humanities/Chemistry': 20 / 16,
               'Grades Specialty': 20 / 20,
               'Other': 1}
