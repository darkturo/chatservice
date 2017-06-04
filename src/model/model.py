import hashlib

from flask_sqlalchemy import SQLAlchemy

# Configure and initialize SQLAlchemy under this Flask webapp.
db = SQLAlchemy()


def calculate_hash(username, password):
    data = "{u}++{p}".format(u=username, p=password)
    return hashlib.sha256(data).hexdigest()[:16]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(16), unique=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = calculate_hash(name, password)

    def __repr__(self):
        return '<User: {n} <{e}>>'.format(n=self.name, e=self.email)


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
