from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_l('Old Password'), validators=[DataRequired()])
    new_password = PasswordField(_l('New Password'), validators=[DataRequired()])
    new_password_confirm = PasswordField(_l('Repeat New Password'), validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField(_l('Change Password'))