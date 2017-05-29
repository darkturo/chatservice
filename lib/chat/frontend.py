from flask import render_template, redirect
from flask_bootstrap import Bootstrap

from chat import app

import chat.navbar


Bootstrap(app)

WebAppName = "ChatRoom"


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


chat.navbar.register(app, WebAppName, 
                         {'Start': 'index', 
                          'About': 'about'})   
