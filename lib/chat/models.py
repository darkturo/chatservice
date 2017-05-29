from sqlalchemy import Column, Integer, String
from chat.database import Base

from hashlib import sha512

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(16), unique=True)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.email = sha512.new(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % (self.name)
