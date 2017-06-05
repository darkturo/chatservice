from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from model import *
import os.path

project_base_dir = os.path.normpath( os.path.join(__file__, "..", ".." ) )
template_folder = os.path.join(project_base_dir, "view", "templates")
static_folder = os.path.join(project_base_dir, "view", "static")


app = Flask(__name__, template_folder=template_folder,
                      static_folder=static_folder)

# Flask WebApp Configuration
app.secret_key = 'bd7a1eec3209ae69dd52df7c2c2dbe5700a67ad5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chat.test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:xxxx@localhost:3306/testdb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:xxxx@localhost:5432/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Flask plugins initialization
bootstrap = Bootstrap(app)
nav = Nav()
nav.init_app(app)
db.init_app(app)


# Create the database tables and records inside a temporary test context
with app.test_request_context():
    load_db(db)

# Import by default
__all__ = ['app', 'nav']


# Load frontend and backend modules and register the (URL routes, func) 
import controller.frontend
import controller.backend
