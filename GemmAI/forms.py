

from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name     = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()],)
