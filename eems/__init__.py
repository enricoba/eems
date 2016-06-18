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
from support import sqlite
# from support import detects, checks
from sensors import ds18b20_new


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

    # level-3 :: SESSION
    session = sqlite.DBHandler()
    session.start(global_data['SESSION'])

    if request.method == 'POST':
        session_config_hw, session_config_sw = session.get_session_config()
        session_config_hws_ds18b20 = session.get_session_config_hws()
        if 'hardware-next' in request.form:
            ds18b20_table = {}
            head_flag = list()
            # DS18B20 sensor
            ds18b20_cb = 'ds18b20_cb' in request.form
            if ds18b20_cb is True:
                # TODO anstatt POST-Skript FUnktion über JS ausführen und rückwert bearbeiten.
                # alle rückmeldungen in JS um schneller zu arbeiten und page reloads zu vermeiden
                senssor_ds18b20 = ds18b20_new.DS18B20()
                session_config_hw['display'] = 'true'
                session_config_hws_ds18b20['display'] = 'true'

                # execute check
                senssor_ds18b20.check_w1_modules()
                senssor_ds18b20.check_w1_config()
                check = True
                # if senssor_ds18b20.check_flags_status() is True:
                if check is True:
                    # check sensors
                    ds18b20_sensors = ['1', '2', 'adsad']
                    # sensors = detects.ds18b20_sensors()
                    if len(ds18b20_sensors):
                        tmp_dict = dict()
                        for sensor in ds18b20_sensors:
                            tmp_dict[sensor] = -9999.0
                        # read temperatures
                        # tmp_dict = ds18b20.read_ds18b20(tmp_dict)
                        # return: DICT(sensors, values)

                        # add sensor_ids_table
                        ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
                        if ds18b20_table_check is False:
                            session.add_sensor_ids_table('ds18b20')
                            session.add_sensor_info('ds18b20', tmp_dict)

                        ds18b20_table = tmp_dict
                        session_config_hws_ds18b20['list'] = 'true'
                        session_config_hws_ds18b20['status'] = 'alert-success'
                        session_config_hws_ds18b20['msg_1'] = 'Success!'
                        session_config_hws_ds18b20['msg_2'] = ' - {} DS18B20 ' \
                            'sensors have been detected.'\
                            .format(len(ds18b20_table))
                        head_flag.append('ok')
                    else:
                        session_config_hws_ds18b20['status'] = 'alert-warning'
                        session_config_hws_ds18b20['msg_1'] = 'Warning!'
                        session_config_hws_ds18b20['msg_2'] = ' - No DS18B20 sensors have been detected.'
                        head_flag.append('war')
                else:
                    session_config_hws_ds18b20['status'] = 'alert-danger'
                    session_config_hws_ds18b20['msg_1'] = 'Error!'
                    session_config_hws_ds18b20['msg_2'] = ' - DS18B20 hardware requirements failed.'
                    head_flag.append('error')

            # manage overall status
            if 'error' in head_flag:
                session_config_hw['icon'] = 'fa-exclamation'
                session_config_hw['color'] = 'red'
            elif 'war' in head_flag:
                session_config_hw['icon'] = 'fa-flash'
                session_config_hw['color'] = 'orange'
            elif 'ok' in head_flag:
                session_config_hw['icon'] = 'fa-check'
                session_config_hw['color'] = 'green'
                session_config_hw['final'] = 1

            if session_config_hw['final'] == 1:
                toggle = 'collapse'
            else:
                toggle = 'deactivate'

            # update database
            session.write_session_config(session_config_hw, 'hardware')
            session.write_session_config_hws(session_config_hws_ds18b20)
            session.close()

            # render template
            return render_template('index.html', name='config',
                                   global_data=global_data,
                                   content=content,
                                   ds18b20_vars=session_config_hws_ds18b20,
                                   ds18b20_table=ds18b20_table,
                                   session_config=session_config_hw,
                                   session_config_sw=session_config_sw,
                                   toggle=toggle)
        elif 'software-next' in request.form:
            # get sensors
            ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
            if ds18b20_table_check:
                ds18b20_table = session.get_sensor_info('SENSOR_IDS_DS18B20')
                ds18b20_user_names = session.get_sensor_user_name('SENSOR_IDS_DS18B20')
            else:
                ds18b20_table = {}
                ds18b20_user_names = {}

            # set software_flag
            if session_config_sw['final'] is 0:
                session_config_sw['display'] = 'true'
                session_config_sw['final'] = 1

                tmp_dict = dict()
                for key in ds18b20_table.keys():
                    tmp_dict[key] = request.form[key]

                # todo HIER NOCH EIN FEHLER !
                # was für einer? sehe keinen bisher
                duration = int(request.form['duration'])
                interval = int(request.form['interval'])
                session.write_session_config_sws(duration, interval)
                session.write_session_config(session_config_sw, 'software')
                session.update_user_sensor_names('ds18b20', tmp_dict)
                ds18b20_user_names = tmp_dict
            # close session
            session.close()
            return render_template('index.html', name='monitor',
                                   global_data=global_data,
                                   content=content,
                                   ds18b20_user_names=ds18b20_user_names)
    else:
        session_config_hw, session_config_sw = session.get_session_config()
        session_config_hws_ds18b20 = session.get_session_config_hws()

        duration, interval = session.get_session_config_sws()

        # toggle
        if session_config_hw['final'] == 1:
            toggle = 'collapse'
        else:
            toggle = 'deactivate'
        # check if dsb18 table exist and react
        ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
        if ds18b20_table_check:
            ds18b20_table = session.get_sensor_info('SENSOR_IDS_DS18B20')
            user_names = session.get_sensor_user_name('SENSOR_IDS_DS18B20')
        else:
            ds18b20_table = dict()
            user_names = dict()

        session.close()
        return render_template('index.html', name='config',
                               global_data=global_data,
                               content=content,
                               ds18b20_vars=session_config_hws_ds18b20,
                               ds18b20_table=ds18b20_table,
                               session_config=session_config_hw,
                               session_config_sw=session_config_sw,
                               duration=duration, interval=interval,
                               toggle=toggle,
                               user_names=user_names)


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

    # level-3 :: SESSION
    session = sqlite.DBHandler()
    session.start(global_data['SESSION'])

    ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
    if ds18b20_table_check:
        ds18b20_user_names = session.get_sensor_user_name('SENSOR_IDS_DS18B20')
    else:
        ds18b20_user_names = {}
    session.close()
    return render_template('index.html', name='monitor',
                           global_data=global_data,
                           content=content,
                           ds18b20_user_names=ds18b20_user_names)


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
