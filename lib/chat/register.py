from flask_wtf import FlaskForm, RecaptchaField

from chat import app

from wtforms import Form, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), 
						   Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email(),
						   Length(min=7, max=256)])
    password = PasswordField('New Password', validators=[DataRequired(),
        		EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

