from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ChangePasswordForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash(_('Invalid old password'))
            return redirect(url_for('auth.change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash(_('Your password has been changed.'))
        return redirect(url_for('auth.change_password'))
    return render_template('auth/change_password.html', title=_('Change Password'), form=form)