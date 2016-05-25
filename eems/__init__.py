# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

# import external modules
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for


# import eems modules
from support import sqlite
# from support import detects, checks
# from sensors import ds18b20


"""
eems project information
"""

__project__ = 'eems'
__version__ = '0.2.0.1b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


# Flask object
app = Flask(__name__)


# global template data
global_data = {
    'version':              __version__,
    'session':              'None',
    'navbar_status':        '',
    'session_icon':         '',
    'session_color':        ''
}


@app.route('/', methods=['GET', 'POST'])
def index():
    # level-0 :: VARIABLES
    global global_data

    # level-1 :: CONFIG
    config_db = sqlite.ConfigHandler()
    config_db.start()
    global_data['session'] = config_db.get('SESSION')
    global_data['navbar_status'] = config_db.get('NAVBAR_STATUS')
    global_data['session_icon'] = config_db.get('SESSION_ICON')
    global_data['session_color'] = config_db.get('SESSION_COLOR')
    home = config_db.get('HOME')
    config_db.close()

    profiles = ['new']
    tmp = os.listdir(home)
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
                                 '{}/{}.db'.format(home, profile_tmp)])
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
            config_db.write('SESSION', 'None')
            config_db.write('NAVBAR_STATUS', 'disabled')
            config_db.write('SESSION_ICON', 'unlock')
            config_db.write('SESSION_COLOR', 'darkred')
            config_db.close()

            # handle session status
            global_data['session'] = 'None'
            global_data['navbar_status'] = 'disabled'
            global_data['session_icon'] = 'unlock'
            global_data['session_color'] = 'darkred'
            return render_template('index.html', name='index',
                                   global_data=global_data,
                                   profiles=profiles, len=len(profiles))
    else:
        return render_template('index.html', name='index',
                               global_data=global_data,
                               profiles=profiles, len=len(profiles))


@app.route('/config/', methods=['GET', 'POST'])
def config():
    # level-0 :: VARIABLES
    global global_data

    # level-1 :: CONFIG
    config_db = sqlite.ConfigHandler()
    config_db.start()
    global_data['session'] = config_db.get('SESSION')
    global_data['navbar_status'] = config_db.get('NAVBAR_STATUS')
    global_data['session_icon'] = config_db.get('SESSION_ICON')
    global_data['session_color'] = config_db.get('SESSION_COLOR')
    config_db.close()

    # level-2 :: SESSION
    session = sqlite.DBHandler()
    session.start(global_data['session'])

    if request.method == 'POST':
        session_config_hw, session_config_sw = session.get_session_config()
        session_config_hws_ds18b20 = session.get_session_config_hws()
        if 'hardware-next' in request.form:
            ds18b20_table = {}
            head_flag = list()
            # DS18B20 sensor
            ds18b20_cb = 'ds18b20_cb' in request.form
            if ds18b20_cb is True:
                session_config_hw['display'] = 'true'
                session_config_hws_ds18b20['display'] = 'true'

                # execute check
                # c = checks.Check()
                check = True
                # if c.w1_config() is True and c.w1_modules() is True:
                if check is True:
                    # check sensors
                    sensors = ['1', '2', 'adsad']
                    # sensors = detects.ds18b20_sensors()
                    if len(sensors):
                        tmp_dict = dict()
                        for sensor in sensors:
                            tmp_dict[sensor] = -9999.0
                        # read temperatures
                        # tmp_dict = ds18b20.read_ds18b20(tmp_dict)
                        # return: DICT(sensors, values)

                        # add sensor_ids_table
                        ds18b20_table_check = session.check_table_exist(
                            'SENSOR_IDS_DS18B20')
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
                        session_config_hws_ds18b20['msg_2'] = ' - No DS18B20 ' \
                            'sensors have been detected.'
                        head_flag.append('war')
                else:
                    session_config_hws_ds18b20['status'] = 'alert-danger'
                    session_config_hws_ds18b20['msg_1'] = 'Error!'
                    session_config_hws_ds18b20['msg_2'] = ' - DS18B20 ' \
                        'hardware requirements failed.'
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
                                   ds18b20_vars=session_config_hws_ds18b20,
                                   ds18b20_table=ds18b20_table,
                                   session_config=session_config_hw,
                                   session_config_sw=session_config_sw,
                                   toggle=toggle)
        elif 'software-next' in request.form:
            # get sensors
            ds18b20_table_check = session.check_table_exist(
                'SENSOR_IDS_DS18B20')
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

    # level-1 :: CONFIG
    config_db = sqlite.ConfigHandler()
    config_db.start()
    global_data['session'] = config_db.get('SESSION')
    global_data['navbar_status'] = config_db.get('NAVBAR_STATUS')
    global_data['session_icon'] = config_db.get('SESSION_ICON')
    global_data['session_color'] = config_db.get('SESSION_COLOR')
    config_db.close()

    # level-2 :: SESSION
    session = sqlite.DBHandler()
    session.start(global_data['session'])

    ds18b20_table_check = session.check_table_exist(
        'SENSOR_IDS_DS18B20')
    if ds18b20_table_check:
        ds18b20_user_names = session.get_sensor_user_name('SENSOR_IDS_DS18B20')
    else:
        ds18b20_user_names = {}
    session.close()
    return render_template('index.html', name='monitor',
                           global_data=global_data,
                           ds18b20_user_names=ds18b20_user_names)


@app.route('/licence/')
def licence():
    # level-0 :: VARIABLES
    global global_data

    # level-1 :: CONFIG
    config_db = sqlite.ConfigHandler()
    config_db.start()
    global_data['session'] = config_db.get('SESSION')
    global_data['session'] = config_db.get('SESSION')
    global_data['navbar_status'] = config_db.get('NAVBAR_STATUS')
    global_data['session_icon'] = config_db.get('SESSION_ICON')
    global_data['session_color'] = config_db.get('SESSION_COLOR')
    config_db.close()
    return render_template('index.html', name='licence',
                           global_data=global_data)


if __name__ == "__main__":
    # in deployment MUST be False !!!
    app.debug = True
    app.run()
