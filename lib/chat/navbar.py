from flask_nav import Nav
from flask_nav.elements import Navbar, View


def register(flask_app, web_app_name, views_dict):
    nav = Nav()

    views = [ View(name, funct) for name, funct in views_dict.iteritems() ]
    
    @nav.navigation()
    def mynavbar():
        return Navbar(web_app_name, *views)

    nav.init_app(flask_app)
