from flask import render_template, redirect, request
from flask_bootstrap import Bootstrap

from chat import app
from chat.register import RegistrationForm
from chat.database import init_db, db_session

import chat.navbar



bootstrap = Bootstrap(app)

WebAppName = "ChatRoom"


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if request.method == 'POST' and register_form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
	db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=register_form)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


chat.database.init_db()
chat.navbar.register(app, WebAppName, 
                         {'Start': 'index', 
                          'About': 'about'})   
