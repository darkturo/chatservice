from view.forms import *


class ChatForm(Form):
    conversation = TextField('Chat')
    message = StringField('Message')
