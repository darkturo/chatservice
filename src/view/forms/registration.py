from view.forms import *


class RegistrationForm(Form):
    username = StringField('Username', validators=[Required(), 
						   Length(min=4, max=50)])
    email = StringField('Email Address', validators=[Required(), Email(),
						   Length(min=7, max=120)])
    password = PasswordField('New Password', validators=[Required(),
        		EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
