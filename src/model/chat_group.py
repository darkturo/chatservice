from model import db

class ChatGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    public_key = db.Column(db.String(4000))
    private_key = db.Column(db.String(1000))

    def __init__(self, name=None, public=None, password=None):
        self.name = name
        self.private_key = private_key
        self.public_key = public_key

    def __repr__(self):
        return '<Group: {n}>'.format(n=self.name)
