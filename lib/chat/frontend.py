from flask import render_template, redirect, url_for, request, flash, session, g
from flask_bootstrap import Bootstrap
from flask_nav import Nav
#from flask_nav.elements import Navbar, View, Subgroup
from flask_nav.elements import *

from chat import app
from chat.forms import RegistrationForm, LoginForm
from chat.database import init_db, db_session
from chat.models import User

import chat


WebAppName = "Chat Service"


# Flask plugins initialization
bootstrap = Bootstrap(app)
nav = Nav()
nav.init_app(app)


# WebApplication frontend
@app.route('/', methods=['GET'])
def index():
    if g.user:
        print "Entro %s" % g.user.name
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
        if user:
            if user.password == form.password.data:
                user.logged_in = True
                db_session.add(user)
                db_session.commit()
                session['user_id'] = user.name
                return redirect(url_for('index'))
    return render_template('login.html', form=form, form_name="login_form")


@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        g.user.logged_in = False
        db_session.add(g.user)
        db_session.commit()
        g.user = None
        del session['user_id']
    return redirect(url_for('index'))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/chat', methods=['GET'])
@app.route('/chat/<chat_room_id>', methods=['GET'])
def group_chat(chat_room_id=None):
    if not g.current_chat_group and not chat_room_id:
        chat_room_id = create_chat_room()

    if not chat_room_id:
        chat_room_id = g.current_chat_group

    chat_group = ChatGroup.query.filter_by(groupid=chat_room_id).first_or_404()
    g.current_chat_group = chat_room_id

    #chat = Chat.query.filter_by(chid=chat_room_id).first()
    return render_template('chat.html', name=chat_group.name, 
                           public_key=chat_group.public_key,
                           chat_id=chat_room_id)


@app.route('/create_chat_room', methods=['GET'])
def create_chat_room():
    form = ChatGroupCreationForm(request.form)
    if request.method == 'POST' and form.validate():
        chatgroupn = ChatGroup(form.groupname.data)
        db_session.add(chatgroup)
        db_session.commit()
        return redirect(url_for('/chat/{cid}'.format(cid=chatgroup.id)))
    return render_template('create_chat_room.html', form=form)


@app.route('/chat', methods=['GET'])


@app.route('/dm', methods=['GET'])
@app.route('/dm/<target_user_id>', methods=['GET'])
def direct_message(target_user_id=None):
    pass


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id=None):
    pass


# Other stuff
# FIXME: I have to move this code elsewhere. Perhaps reorganise the lib better
#        using the model/view/controller concept.
#        Somethings though seem difficult to move away...

@nav.navigation()
def mynavbar():
    views = []
    if 'user_id' in session:
        views = [ View('Group Chat', 'group_chat'),
                  View('Direct Message', 'direct_message'),
                  View('About', 'about'),
                  Subgroup(session['user_id'],
                         View('Profile', 'profile'),
                         View('Logout', 'logout')
                  ) ]
    else:
        views = [ View('Start', 'index'), View('Login', 'login'),
                  View('Register', 'register'), View('About', 'about') ]

    return Navbar(WebAppName, *views)



@app.before_request
def load_user():
    if 'user_id' in session:
        user = User.query.filter_by(name=session["user_id"]).first()
    else:
        user = None

    g.user = user


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


chat.database.init_db()
