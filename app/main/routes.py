from flask import render_template, flash, redirect, url_for
from flask_login import login_required
import json

from .. import db
from ..models import Teacher, Course, Responsibility, multipliers
from .forms import AddTeacherForm, AddCourseForm, AddResponsibilityForm, AssignMemberForm, AssignTeacherForm,  \
    AssignCourseForm, AssignResponsibilityForm, ChangeCourseForm, ChangeTeacherForm, ChangeResponsibilityForm, \
    ChangeMultipliersForm, ChooseViewForm, SearchCourseForm
from . import bp
from .course_conversion import course_conversion

'''
@bp.before_app_first_request
def update_schema():
    course_conversion()
'''


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/teacher_list', methods=['GET', 'POST'])
@login_required
def teacher_list():
    title = 'Teacher Load Summary'
    if Teacher.query.first():
        teachers = Teacher.query.order_by('last_name').all()
    else:
        flash('No teachers have been added yet.')
        return redirect(url_for('main.adds'))
    form = ChooseViewForm()
    if form.validate_on_submit():
        if form.view_hs.data:
            teachers = Teacher.query.filter_by(
                hs=True).order_by('last_name').all()
            teachers = [
                teacher for teacher in teachers if teacher.teaching_load_p() > 75]
            title = 'High School Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_grades.data:
            teachers = Teacher.query.filter_by(
                grades=True).order_by('last_name').all()
            teachers = [
                teacher for teacher in teachers if teacher.teaching_load_p() > 75]
            title = 'Grades Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_ft.data:
            teachers = Teacher.query.order_by('last_name').all()
            teachers = [
                teacher for teacher in teachers if teacher.teaching_load_p() > 75]
            title = 'FT Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_pt.data:
            teachers = Teacher.query.order_by('last_name').all()
            teachers = [
                teacher for teacher in teachers if teacher.teaching_load_p() < 75]
            title = 'PT Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_hum.data:
            teachers = Teacher.query.order_by('last_name').all()
            hum_dep = ['Zinn', 'Blanchard', 'Fretz', 'Humanities']
            teachers = [
                teacher for teacher in teachers if teacher.last_name in hum_dep]
            title = 'Humanities Department Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)
        elif form.view_all.data:
            teachers = Teacher.query.order_by('last_name').all()
            title = 'Teacher Load Summary'
            return render_template('teacher_list.html', title=title, teachers=teachers, form=form)

    return render_template('teacher_list.html', title=title, teachers=teachers, form=form)


@bp.route('/teacher_view/<tid>', methods=['GET', 'POST'])
@login_required
def teacher_view(tid):
    teacher = Teacher.query.filter_by(id=tid).first()
    title = 'Teacher View: {} {}'.format(teacher.first_name, teacher.last_name)

    form_a = AssignCourseForm()
    form_a.course_id.choices = [(c.id, c.title)
                                for c in Course.query.order_by('title')]
    if form_a.validate_on_submit():
        course_id = form_a.course_id.data
        course = Course.query.filter_by(id=course_id).first()
        if form_a.assign.data:
            if teacher not in course.teachers:
                course.teachers.append(teacher)
                db.session.add(teacher)
                db.session.commit()
                flash('Course assigned.')
            else:
                flash('Teacher already assigned to this course.')
        elif form_a.remove.data:
            if teacher in course.teachers:
                course.teachers.remove(teacher)
                db.session.add(course)
                db.session.commit()
                flash('Course removed.')
        return redirect(url_for('main.teacher_view', tid=teacher.id))

    form_c = ChangeTeacherForm(obj=teacher)
    if form_c.validate_on_submit():
        if form_c.change.data:
            form_c.populate_obj(teacher)
            db.session.commit()
            flash('Updates applied.')
        if form_c.delete.data:
            for resp in teacher.responsibilities.all():
                resp.members.remove(teacher)
            db.session.commit()
            db.session.delete(teacher)
            db.session.commit()
            flash('Teacher removed from database.')
        return redirect(url_for('main.teacher_list'))

    form_r = AssignResponsibilityForm(obj=teacher)
    form_r.resp_id.choices = [(r.id, r.name)
                              for r in Responsibility.query.order_by('name')]
    if form_r.validate_on_submit():
        resp_id = form_r.resp_id.data
        resp = Responsibility.query.filter_by(id=resp_id).first()
        if form_r.assign.data:
            if teacher not in resp.members:
                resp.members.append(teacher)
                db.session.add(resp)
                db.session.commit()
                flash('Responsibility assigned.')
            else:
                flash('Teacher already assigned to this responsibility.')
        elif form_r.remove.data:
            if teacher in resp.members:
                resp.members.remove(teacher)
                db.session.add(resp)
                db.session.commit()
            flash('Responsibility removed.')
        return redirect(url_for('main.teacher_view', tid=teacher.id))

    return render_template('teacher_view.html',
                           teacher=teacher,
                           courses=teacher.courselist.order_by('title'),
                           resps=teacher.responsibilities.order_by('name'),
                           title=title,
                           form_a=form_a, form_c=form_c, form_r=form_r)


@bp.route('/course_list', methods=['GET', 'POST'])
@login_required
def course_list():
    title = 'Course List'
    if Course.query.first():
        courses = Course.query.order_by('title').all()
    else:
        flash('No courses have been added yet.')
        return redirect(url_for('main.adds'))

    form = SearchCourseForm()
    if form.validate_on_submit():
        s = form.string_box.data.split()
        courses = []
        for i in s:
            courses.append(Course.query.filter(
                Course.title.like('%' + i + '%')).all())
        courses = [course for sublist in courses for course in sublist]
        return render_template('course_list.html', title='Course List', courses=courses, form=form)

    return render_template('course_list.html', title=title, courses=courses, form=form)


@bp.route('/course_view/<cid>', methods=['GET', 'POST'])
@login_required
def course_view(cid):
    course = Course.query.filter_by(id=cid).first()
    title = 'Course View: {}'.format(course.title)

    form_c = ChangeCourseForm(obj=course)
    if form_c.validate_on_submit():
        if form_c.assign.data:
            form_c.populate_obj(course)
            db.session.commit()
            flash('Updates applied.')
            return redirect(url_for('main.course_view', cid=course.id))
        elif form_c.delete.data:
            for teacher in course.teachers:
                course.teachers.remove(teacher)
            db.session.commit()
            db.session.delete(course)
            db.session.commit()
            flash('Course removed from database.')
            return redirect(url_for('main.course_list'))

    form_a = AssignTeacherForm(obj=course)
    form_a.teacher_id.choices = [(t.id, t.last_name + ', ' + t.first_name)
                                 for t in Teacher.query.order_by('last_name')]
    if form_a.validate_on_submit():
        teacher = Teacher.query.filter_by(id=form_a.teacher_id.data).first()
        if form_a.assign.data:
            if teacher not in course.teachers:
                course.teachers.append(teacher)
                db.session.add(course)
                db.session.commit()
                flash('Teacher assigned.')
                return redirect(url_for('main.course_view', cid=course.id))
            else:
                flash('Teacher already assigned to that course.')
                return redirect(url_for('main.course_view', cid=course.id))
        elif form_a.remove.data:
            if teacher in course.teachers:
                course.teachers.remove(teacher)
                db.session.add(course)
                db.session.commit()
                flash('Teacher removed from course.')
                return redirect(url_for('main.course_view', cid=course.id))
            else:
                flash("Teacher wasn't assigned to that course.")
                return redirect(url_for('main.course_view', cid=course.id))

            return redirect(url_for('main.course_list'))

    return render_template('course_view.html', course=course, title=title, form_c=form_c, form_a=form_a)


@bp.route('/responsibility_list', methods=['GET', 'POST'])
@login_required
def responsibility_list():
    title = 'Responsibility List'
    if Responsibility.query.first():
        resps = Responsibility.query.order_by('name').all()
    else:
        flash('No responsibilities have been added yet.')
        return redirect(url_for('main.adds'))

    return render_template('responsibility_list.html', title=title, resps=resps)


@bp.route('/responsibility_view/<rid>', methods=['GET', 'POST'])
@login_required
def responsibility_view(rid):
    resp = Responsibility.query.filter_by(id=rid).first()
    title = 'Responsibility View: {}'.format(resp.name)

    form_a = AssignMemberForm()
    form_a.teacher_id.choices = [(t.id, t.last_name + ', ' + t.first_name)
                                 for t in Teacher.query.order_by('last_name')]
    if form_a.validate_on_submit():
        teacher = Teacher.query.filter_by(id=form_a.teacher_id.data).first()
        if form_a.assign.data:
            if teacher not in resp.members:
                resp.members.append(teacher)
                db.session.add(resp)
                db.session.commit()
                flash('Responsibility assigned.')
            else:
                flash('Teacher already assigned to this responsibility.')
        elif form_a.remove.data:
            if teacher in resp.members:
                resp.members.remove(teacher)
                db.session.add(resp)
                db.session.commit()
                flash('Member removed.')
        return redirect(url_for('main.responsibility_view', rid=resp.id))

    form_c = ChangeResponsibilityForm(obj=resp)
    if form_c.validate_on_submit():
        if form_c.change.data:
            form_c.populate_obj(resp)
            db.session.commit()
            flash('Updates applied.')
            return redirect(url_for('main.responsibility_view', rid=resp.id))
        elif form_c.delete.data:
            for member in resp.members:
                resp.members.remove(member)
            db.session.commit()
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
        flash('{} {} added to teacher list.'.format(
            teacher.first_name, teacher.last_name))
        return redirect(url_for('main.adds'))

    r_form = AddResponsibilityForm()
    if r_form.validate_on_submit():
        if Responsibility.query.filter(Responsibility.name == r_form.name.data).first():
            flash('{} already exists'.format(r_form.name.data))
            return redirect(url_for('main.responsibility_view',
                                    rid=Responsibility.query.filter(Responsibility.name == r_form.name.data).first().id))
        else:
            resp = Responsibility(name=r_form.name.data, hours_per_month=r_form.hours_per_month.data,
                                  months_per_year=r_form.months_per_year.data)
            db.session.add(resp)
            db.session.commit()
            flash('{} added to responsibilities list.'.format(resp.name))
            return redirect(url_for('main.adds'))

    c_form = AddCourseForm()
    try:
        c_form.teacher_id.choices = [(0, "---")] + [(t.id, t.last_name + ", " + t.first_name)
                                                    for t in Teacher.query.order_by('last_name')]
    except:
        c_form.teacher_id.choices = []
    if c_form.validate_on_submit():
        if Course.query.filter(Course.title == c_form.title.data).first():
            flash('{} already exists'.format(c_form.title.data))
            return redirect(url_for('main.course_view',
                                    cid=Course.query.filter(Course.title == c_form.title.data).first().id))
        else:
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
    class MyDict(dict):
        pass

    mult = MyDict(multipliers)
    mult.grades_ML = mult['Grades Main Lesson']
    mult.weeks_year = mult['weeks/year']
    mult.ft_exp = mult['FT Expectation']
    mult.recess = mult['Recess/Lunch']
    mult.arts_movement = mult['Arts/Movement']
    mult.fl = mult['Foreign Language']
    mult.stem = mult['STEM']
    mult.hum_chem = mult['Humanities/Chemistry']
    mult.grades_spec = mult['Grades Specialty']
    mult.other = mult['Other']

    form = ChangeMultipliersForm(obj=mult)
    title = 'Change Multipliers'
    if form.validate_on_submit():

        multipliers['Grades Main Lesson'] = form.grades_ML.data
        multipliers['weeks/year'] = form.weeks_year.data
        multipliers['FT Expectation'] = form.ft_exp.data
        multipliers['Recess/Lunch'] = form.recess.data
        multipliers['Arts/Movement'] = form.arts_movement.data
        multipliers['Foreign Language'] = form.fl.data
        multipliers['STEM'] = form.stem.data
        multipliers['Humanities/Chemistry'] = form.hum_chem.data
        multipliers['Grades Specialty'] = form.grades_spec.data
        multipliers['Other'] = form.other.data

        with open('app/multipliers.json', 'w') as file:
            json.dump(multipliers, file)

        flash('Multipliers updated successfully.')
        return redirect(url_for('main.change_multipliers'))

    return render_template('change_multipliers.html', title=title, form=form)
