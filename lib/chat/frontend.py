from flask import render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap

from chat import app
from chat.forms import RegistrationForm, LoginForm
from chat.database import init_db, db_session
from chat.models import User

import chat.navbar



bootstrap = Bootstrap(app)

WebAppName = "ChatRoom"


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, 
                     form.email.data,
                     form.password.data)
        db_session.add(user)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(name=form.username.data).first()
        if user.password == form.password.data:
            return redirect(url_for('index'))
    return render_template('login.html', form=form, form_name="login_form")


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
