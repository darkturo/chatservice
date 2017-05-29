from flask import Flask
import os.path

project_base_dir = os.path.normpath( os.path.join(__file__, "..", "..", ".." ) )
template_folder = os.path.join(project_base_dir, "templates")

app = Flask(__name__, template_folder=template_folder)
app.secret_key = 'bd7a1eec3209ae69dd52df7c2c2dbe5700a67ad5'

