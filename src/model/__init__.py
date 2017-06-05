from flask_sqlalchemy import SQLAlchemy


# Configure and initialize SQLAlchemy under this Flask webapp.
db = SQLAlchemy()


from user import User
from chat_group import ChatGroup
__all__ =   ['User', 'ChatGroup', 'db', 'load_db']


def load_db(db):
    """Load the database tables and records"""
    # Drop and re-create all the tables
    db.drop_all()
    db.create_all()
