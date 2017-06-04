from view.forms import *


class ChatGroupCreationForm(Form):
    groupname = StringField('Chat Group Name', validators=[Required(), 
                                                           Length(min=3, max=50)])
