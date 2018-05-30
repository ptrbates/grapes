from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ChangeUserForm
from app.models import User
from app.auth.email import send_password_reset_email
from flask_login import login_required


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    title = 'Register New User'
    users = User.query.all()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        if user in User.query.all():
            flash('User {} already exists.'.format(user.username))
            return redirect(url_for('auth.register'))
        else:
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User {} added to database.'.format(user.username))
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', title=title, form=form, users=users)


@bp.route('/user_view/<uid>', methods=['GET', 'POST'])
@login_required
def user_view(uid):
    user = User.query.filter_by(id=uid).first()
    title = 'User View: {}'.format(user.username)

    form = ChangeUserForm(obj=user)
    if form.change.data:
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('User {} updated successfully'.format(user.username))
        return redirect(url_for('auth.user_view', uid=user.id))
    if form.delete.data:
        if user.id == current_user.id:
            flash('{} is currently logged in; cannot delete at this time.'.format(user.username))
            return redirect(url_for('auth.user_view', uid=user.id))
        else:
            db.session.delete(user)
            db.session.commit()
            flash('User {} removed from database'.format(user.username))
            return redirect(url_for('auth.register'))

    return render_template('auth/user_view.html', title=title, user=user, form=form)



@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
