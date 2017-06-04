from view.forms import *


class LoginForm(Form):
    username = StringField('Username', validators=[Required(), 
						   Length(min=4, max=25)])
    password = PasswordField('Password', validators=[Required()])
