# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

# import external modules
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# import eems modules
from sensors import ds18b20


"""
eems project information
"""


__project__ = 'eems'
__version__ = '0.2.0.1b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


# Flask object
app = Flask(__name__)
# check if server or development environment
if os.path.exists('/var/www/eems/eems/data/db/'):
    path = '/var/www/eems/eems/data/db/config.db'
else:
    path = '{}/data/db/config.db'.format(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}'.format(path)
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
db = SQLAlchemy(app)


class General(db.Model):
    __tablename__ = 'General'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    item = db.Column(db.Text)
    value = db.Column(db.Text)

    def __init__(self, item=None, value=None):
        self.item = item
        self.value = value


class Content(db.Model):
    __tablename__ = 'Content'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    position = db.Column(db.Text)
    german = db.Column(db.Text)
    english = db.Column(db.Text)

    def __init__(self, position=None, german=None, english=None):
        self.position = position
        self.german = german
        self.english = english


class Sessions(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    session = db.Column(db.Text)
    data_id = db.Column(db.Text)

    def __init__(self, session=None, data_id=None):
        self.session = session
        self.data_id = data_id


def __db_content(lang):
    tmp_dict = dict()
    content = Content.query.all()
    for i in content:
        if lang == 'de':
            tmp_dict[i.position] = i.german
        elif lang == 'en':
            tmp_dict[i.position] = i.english
    return tmp_dict


def __db_general():
    tmp_dict = dict()
    general = General.query.all()
    for i in general:
        tmp_dict[i.item] = i.value
    return tmp_dict


@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:lang>/', methods=['GET', 'POST'])
def index(lang=None):
    # level-0 :: CONFIG
    global_data = __db_general()

    # level-1 :: CONTENT
    if lang is None:
        content = __db_content(global_data['LANGUAGE'])
    else:
        content = __db_content(lang)

    profiles = ['new']
    sessions = Sessions.query.all()
    for i in sessions:
        profiles.append(i.session.encode("utf-8"))

    if request.method == 'POST':
        if 'session-start' in request.form:
            # get new session input
            profile_tmp = request.form['session-input']

            # verify if new session (input text has a length) or existing session (length = 0)
            if len(profile_tmp):
                session = General.query.filter_by(item='SESSION').first()
                session.value = profile_tmp
                session_add = Sessions(profile_tmp, 1)
                db.session.add(session_add)

                # add default tables and contents
                path = os.path.dirname(__file__)
                subprocess.call(['cp', '{}/data/db/default.db'.format(path),
                                 '{}/{}.db'.format(global_data['HOME'], profile_tmp)])
            else:
                profile_load = request.form['session-load']
                session = General.query.filter_by(item='SESSION').first()
                session.value = profile_load

            # update session related information
            status = General.query.filter_by(item='NAVBAR_STATUS').first()
            icon = General.query.filter_by(item='SESSION_ICON').first()
            color = General.query.filter_by(item='SESSION_COLOR').first()
            status.value = ''
            icon.value = 'lock'
            color.value = 'green'
            db.session.commit()
            return redirect(url_for('config'))
        elif 'sessionLogout' in request.form:
            session = General.query.filter_by(item='SESSION').first()
            status = General.query.filter_by(item='NAVBAR_STATUS').first()
            icon = General.query.filter_by(item='SESSION_ICON').first()
            color = General.query.filter_by(item='SESSION_COLOR').first()
            session.value = '-'
            status.value = 'disabled'
            icon.value = 'unlock'
            color.value = 'darkred'
            db.session.commit()

            # handle session status
            global_data = __db_general()
            return render_template('index.html', name='index',
                                   global_data=global_data,
                                   content=content,
                                   profiles=profiles, len=len(profiles))
    else:
        return render_template('index.html', name='index',
                               global_data=global_data,
                               content=content,
                               profiles=profiles, len=len(profiles))


@app.route('/config/', methods=['GET', 'POST'])
@app.route('/<string:lang>/config/', methods=['GET', 'POST'])
def config(lang=None):
    # level-0 :: CONFIG
    global_data = __db_general()

    # level-1 :: CONTENT
    if lang is None:
        content = __db_content(global_data['LANGUAGE'])
    else:
        content = __db_content(lang)

    # level-2 :: HANDLING
    if request.method == 'POST':
        return render_template('index.html', name='config',
                               global_data=global_data,
                               content=content)
    else:
        return render_template('index.html', name='config',
                               global_data=global_data,
                               content=content)


@app.route('/monitor/')
@app.route('/<string:lang>/monitor/')
def monitor(lang=None):
    # level-0 :: CONFIG
    global_data = __db_general()

    # level-1 :: CONTENT
    if lang is None:
        content = __db_content(global_data['LANGUAGE'])
    else:
        content = __db_content(lang)

    return render_template('index.html', name='monitor',
                           global_data=global_data,
                           content=content)


@app.route('/licence/')
@app.route('/<string:lang>/licence/')
def licence(lang=None):
    # level-0 :: CONFIG
    global_data = __db_general()

    # level-1 :: CONTENT
    if lang is None:
        content = __db_content(global_data['LANGUAGE'])
    else:
        content = __db_content(lang)
    return render_template('index.html', name='licence',
                           global_data=global_data,
                           content=content)


if __name__ == "__main__":
    # in deployment MUST be False !!!
    app.debug = True
    app.run()
