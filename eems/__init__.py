# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

# import external modules
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from support.database import init_db, db_session
from support.models import General, Content

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

# init database connection
init_db()
# test = General.query.all()
# for x in test:
#     print x.item


# close db when app is shutting down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# global template data
global_data = {
    'USER':                 '',
    'HOME':                 '',
    'SESSION':              '-',
    'VERSION':              __version__,
    'NAVBAR_STATUS':        '',
    'SESSION_ICON':         '',
    'SESSION_COLOR':        '',
    'LANGUAGE':             'en',
}

content = {
    'INDEX_CONFIG':         '',
    'INDEX_MONITOR':        '',
    'INDEX_SESSION':        '',
    'INDEX_DOCU':           '',
    'INDEX_LICENCE':        '',
    'INDEX_VERSION':        '',
    'INDEX_LANGUAGE':       '',
    'INDEX_LANGUAGE_DE':    '',
    'INDEX_LANGUAGE_EN':    ''
}


def __db_content(lang):
    """Private function *__db_content* queries the database and reads the content information related to each language.

    :param lang:
        Expects a *string* conainting a language code ('de' / 'en').
    :return:
        Returns *None*.
    """
    cms = Content.query.all()
    for i in cms:
        if lang == 'de':
            content[i.position] = i.german
        elif lang == 'en':
            content[i.position] = i.english


def __db_general():
    kms = General.query.all()
    for i in kms:
        global_data[i.item] = i.value


@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:lang>/', methods=['GET', 'POST'])
def index(lang=None):
    # level-0 :: VARIABLES
    global global_data
    global content

    # level-1 :: CONFIG
    __db_general()

    # level-2 :: CONTENT
    if lang is None:
        __db_content(global_data['LANGUAGE'])
    else:
        __db_content(lang)

    profiles = ['new']
    tmp = os.listdir(global_data['HOME'])
    for profile in tmp:
        profiles.append(str(profile[:-3]))

    if request.method == 'POST':
        if 'session-start' in request.form:
            profile_tmp = request.form['session-input']
            config_db = sqlite.ConfigHandler()
            config_db.start()
            if len(profile_tmp):
                config_db.write('SESSION', profile_tmp)

                # add default tables and contents
                path = os.path.dirname(__file__)
                subprocess.call(['cp', '{}/data/db/default.db'.format(path),
                                 '{}/{}.db'.format(global_data['HOME'], profile_tmp)])
            else:
                profile_load = request.form['session-load']
                config_db.write('SESSION', profile_load)

            config_db.write('NAVBAR_STATUS', '')
            config_db.write('SESSION_ICON', 'lock')
            config_db.write('SESSION_COLOR', 'green')
            config_db.close()
            return redirect(url_for('config'))
        elif 'sessionLogout' in request.form:
            # TODO only redirect to monitor if config is all done!
            # and disable monitor permanently when config unfinished

            config_db = sqlite.ConfigHandler()
            config_db.start()
            config_db.write('SESSION', '-')
            config_db.write('NAVBAR_STATUS', 'disabled')
            config_db.write('SESSION_ICON', 'unlock')
            config_db.write('SESSION_COLOR', 'darkred')
            config_db.close()

            # handle session status
            global_data['SESSION'] = '-'
            global_data['NAVBAR_STATUS'] = 'disabled'
            global_data['SESSION_ICON'] = 'unlock'
            global_data['SESSION_COLOR'] = 'darkred'
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
    # level-0 :: VARIABLES
    global global_data
    global content

    # level-1 :: CONFIG
    __db_general()

    # level-2 :: CONTENT
    __db_content(lang)

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
def monitor():
    # level-0 :: VARIABLES
    global global_data
    global content

    # level-1 :: CONFIG
    __db_general()

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
def licence():
    # level-0 :: VARIABLES
    global global_data
    global content

    # level-1 :: CONFIG
    __db_general()
    return render_template('index.html', name='licence',
                           global_data=global_data,
                           content=content)


if __name__ == "__main__":
    # in deployment MUST be False !!!
    app.debug = True
    app.run()
