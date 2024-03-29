from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth.forms import LoginFrom, RegistrationForm
from app.models import User
from app.auth import bp

@bp.route('login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(
                'Неправильное имя пользователя или пароль пожалуйста проверьте введенные данные и попробуйте еще раз!',
                'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Пользователь {} зашел успешно. {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Вход', form=form)

@bp.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем {} вы успешно зарегистрировались!'.format(form.username.data))
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('auth/register.html', form=form, title='Регистрация')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))