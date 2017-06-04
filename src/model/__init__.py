from flask_sqlalchemy import SQLAlchemy


# Configure and initialize SQLAlchemy under this Flask webapp.
db = SQLAlchemy()


from user import User
from chat_group import ChatGroup
__all__ =   ['User', 'ChatGroup', 'db']
