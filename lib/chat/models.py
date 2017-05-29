import hashlib

from sqlalchemy import Column, Integer, String
from chat.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(16), unique=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = hashlib.sha512(password).hexdigest()[:16]

    def __repr__(self):
        return '<User %r>' % (self.name)
