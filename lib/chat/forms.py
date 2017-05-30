from flask_wtf import FlaskForm, RecaptchaField

from chat import app

from wtforms import Form, BooleanField, StringField, PasswordField, TextField
from wtforms.validators import Required, Length, Email, EqualTo


class RegistrationForm(Form):
    username = StringField('Username', validators=[Required(), 
						   Length(min=4, max=50)])
    email = StringField('Email Address', validators=[Required(), Email(),
						   Length(min=7, max=120)])
    password = PasswordField('New Password', validators=[Required(),
        		EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', validators=[Required(), 
						   Length(min=4, max=25)])
    password = PasswordField('Password', validators=[Required()])


class ChatGroupCreationForm(Form):
    groupname = StringField('Chat Group Name', validators=[Required(), 
                                                           Length(min=3, max=50)])


class ChatForm(Form):
    conversation = TextField('Chat')
    message = StringField('Message')
