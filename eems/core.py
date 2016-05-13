# -*- coding: utf-8 -*-
"""
Server core module
"""

# import external modules
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for


# import eems modules
from __init__ import __version__
from support import sqlite
from support import detects, checks
from sensors import ds18b20


session_name = None
app = Flask(__name__)
# test


@app.route("/", methods=['GET', 'POST'])
def index():
    # get saved profiles
    # henrik
    tmp = os.listdir('/data/F_Projects/F-I_GitHub/eems/eems/data')
    # auro
    # tmp = os.listdir('/Volumes/Tesla/05_Github/eems/eems/data')
    # pipi
    # tmp = os.listdir('/home/pi/eems/data')
    profiles = ['new']
    for i in tmp:
        if i != 'default.db':
            profiles.append(i[:-3])

    # get session name
    global session_name
    # handle session status
    if session_name is None:
        navbar_status = 'disabled'
        session_icon = 'unlock'
        session_color = 'darkred'
    else:
        navbar_status = ''
        session_icon = 'lock'
        session_color = 'green'

    if request.method == 'POST':
        if 'session-start' in request.form:
            profile_tmp = request.form['session-input']
            if len(profile_tmp):
                profiles.append(str(profile_tmp))
                session_name = profile_tmp
                print session_name

                # add default tables and contents
                # pi
                """
                subprocess.call(['cp', '/home/pi/eems/default.db',
                                 '/home/pi/eems/{}.db'.format(session_name)])
                """

                # henrik
                subprocess.call(['cp', '/data/F_Projects/F-I_GitHub/eems/eems/data/default.db',
                                 '/data/F_Projects/F-I_GitHub/eems/eems/data/{}.db'.format(session_name)])

                # auro
                """
                subprocess.call(['cp', '/Volumes/Tesla/05_Github/eems/eems/data/default.db',
                                 '/Volumes/Tesla/05_Github/eems/eems/data/{}.db'.format(session_name)])
                """
                # redirect
                return redirect(url_for('config'))
            else:
                # todo profile laden
                print 'load project'
                session_name = request.form['session-load']
                return redirect(url_for('config'))
        elif 'sessionLogout' in request.form:
            print 'LOGOUT'
            session_name = None
            # handle session status
            navbar_status = 'disabled'
            session_icon = 'unlock'
            session_color = 'darkred'
            return render_template("index.html", name='index',
                                   version=__version__,
                                   profiles=profiles, len=len(profiles),
                                   navbar_status=navbar_status,
                                   session_name=session_name,
                                   session_icon=session_icon,
                                   session_color=session_color)
    else:
        print 'GET: INDEX'
        return render_template("index.html", name='index', version=__version__,
                               profiles=profiles, len=len(profiles),
                               navbar_status=navbar_status,
                               session_name=session_name,
                               session_icon=session_icon,
                               session_color=session_color)


@app.route("/config/", methods=['GET', 'POST'])
def config():
    # get session name
    global session_name
    # handle session status
    if session_name is None:
        navbar_status = 'disabled'
        session_icon = 'unlock'
        session_color = 'darkred'
    else:
        navbar_status = ''
        session_icon = 'lock'
        session_color = 'green'

    session = sqlite.DBHandler()
    session.start(session_name)

    if request.method == 'POST':
        print 'POST'
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
                print 'IN OVERALL STATUS'
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
            return render_template("index.html", name='config',
                                   version=__version__,
                                   ds18b20_vars=session_config_hws_ds18b20,
                                   ds18b20_table=ds18b20_table,
                                   session_config=session_config_hw,
                                   session_config_sw=session_config_sw,
                                   navbar_status=navbar_status,
                                   session_icon=session_icon,
                                   session_color=session_color,
                                   session_name=session_name,
                                   toggle=toggle)
        elif 'software-next' in request.form:
            print 'software button'
            # get sensors
            ds18b20_table_check = session.check_table_exist(
                'SENSOR_IDS_DS18B20')
            if ds18b20_table_check:
                ds18b20_table = session.get_sensor_info('SENSOR_IDS_DS18B20')
            else:
                ds18b20_table = {}

            # set software_flag
            if session_config_sw['final'] is 0:
                session_config_sw['display'] = 'true'
                session_config_sw['final'] = 1

                print 'ds18b20_table before', ds18b20_table
                tmp_dict = dict()
                for key in ds18b20_table.keys():
                    print key, request.form[key]
                    tmp_dict[key] = request.form[key]
                print tmp_dict

                # todo HIER NOCH EIN FEHLER !
                duration = int(request.form['duration'])
                interval = int(request.form['interval'])
                session.write_session_config_sws(duration, interval)
                session.write_session_config(session_config_sw, 'software')
                session.update_user_sensor_names('ds18b20', tmp_dict)
            # close session
            session.close()
            return render_template("index.html", name='monitor',
                                   version=__version__,
                                   session_icon=session_icon,
                                   session_color=session_color,
                                   session_name=session_name)
    else:
        print 'GET'
        session_config_hw, session_config_sw = session.get_session_config()
        session_config_hws_ds18b20 = session.get_session_config_hws()

        duration, interval = session.get_session_config_sws()

        # toggle
        if session_config_hw['final'] == 1:
            toggle = 'collapse'
        else:
            toggle = 'deactivate'
            print toggle
        # check if dsb18 table exist and react
        ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
        if ds18b20_table_check:
            ds18b20_table = session.get_sensor_info('SENSOR_IDS_DS18B20')
            user_names = session.get_sensor_user_name('SENSOR_IDS_DS18B20')
        else:
            ds18b20_table = dict()
            user_names = dict()

        session.close()
        return render_template("index.html", name='config', version=__version__,
                               ds18b20_vars=session_config_hws_ds18b20,
                               ds18b20_table=ds18b20_table,
                               session_config=session_config_hw,
                               session_config_sw=session_config_sw,
                               navbar_status=navbar_status,
                               session_icon=session_icon,
                               session_color=session_color,
                               session_name=session_name,
                               duration=duration, interval=interval,
                               toggle=toggle,
                               user_names=user_names)


@app.route("/monitor/")
def monitor():
    # get session name
    global session_name
    # handle session status
    if session_name is None:
        navbar_status = 'disabled'
        session_icon = 'unlock'
        session_color = 'darkred'
    else:
        navbar_status = ''
        session_icon = 'lock'
        session_color = 'green'
    print 'monitor called'
    return render_template("index.html", name='monitor', version=__version__,
                           navbar_status=navbar_status,
                           session_icon=session_icon,
                           session_color=session_color,
                           session_name=session_name)


@app.route("/licence/")
def licence():
    # get session name
    global session_name
    # handle session status
    if session_name is None:
        navbar_status = 'disabled'
        session_icon = 'unlock'
        session_color = 'darkred'
    else:
        navbar_status = ''
        session_icon = 'lock'
        session_color = 'green'
    return render_template("index.html", name='licence',
                           version=__version__,
                           navbar_status=navbar_status,
                           session_icon=session_icon,
                           session_color=session_color,
                           session_name=session_name
                           )

# host='0.0.0.0'

if __name__ == "__main__":
    app.run()
