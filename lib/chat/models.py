import hashlib

from sqlalchemy import Column, Integer, String
from chat.database import Base

def calculate_hash(username, password):
    data = "{u}++{p}".format(u=username, p=password)
    return hashlib.sha256(data).hexdigest()[:16]


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(16), unique=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = calculate_hash(name, password)

    def __repr__(self):
        return '<User %r>' % (self.name)
