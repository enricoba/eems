# -*- coding: utf-8 -*-
"""
Server core module
"""

# import external modules
import os
# import subprocess
from flask import Flask, render_template, request, redirect, url_for
from shutil import copyfile


# import eems modules
from __init__ import __version__
from support import sqlite
# from support import detects, checks
# from sensors import ds18b20


session_name = None
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    # get saved profiles
    tmp = os.listdir("D:\F_Projects\F-I_GitHub\eems\eems\data")
    # tmp = os.listdir('/Volumes/Tesla/05_Github/eems/eems/data')
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
        profile_tmp = request.form['session-input']
        if len(profile_tmp):
            profiles.append(str(profile_tmp))
            session_name = profile_tmp
            print session_name

            # add default tables and contents
            """
            subprocess.call(['cp', '/home/pi/eems/default.db',
                             '/home/pi/eems/{}.db'.format(profile)])"""

            copyfile('D:/F_Projects/F-I_GitHub/eems/eems/data/default.db',
                     'D:/F_Projects/F-I_GitHub/eems/eems/data/{}.db'
                     .format(session_name))

            """subprocess.call(['cp', '/Volumes/Tesla/05_Github/eems/eems/data/default.db',
                             '/Volumes/Tesla/05_Github/eems/eems/data/{}.db'.format(profile)])"""
            # redirect
            return redirect(url_for('config'))
        else:
            # todo profile laden
            print 'load project'
            session_name = request.form['session-load']
            return redirect(url_for('config'))
    else:
        print profiles
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
    ds18b20_table = {}
    if request.method == 'POST':
        print 'POST'
        session_config = session.get_session_config()
        session_config_hws_ds18b20 = session.get_session_config_hws()
        if 'hardware-next' in request.form:
            head_flag = list()
            # DS18B20 sensor
            ds18b20_cb = 'ds18b20_cb' in request.form
            if ds18b20_cb is True:
                session_config['display'] = 'true'
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
                            tmp_dict[sensor] = -9999
                        # read temperatures
                        # tmp_dict = ds18b20.read_ds18b20(tmp_dict)
                        # return: DICT(sensors, values)

                        # add sensor_ids_table
                        session.add_sensor_ids_table('ds18b20')
                        session.add_sensor_info('ds18b20', tmp_dict)

                        # ds18b20_vars['sensors'] = tmp_dict
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
                session_config['icon'] = 'fa-exclamation'
                session_config['color'] = 'red'
            elif 'war' in head_flag:
                session_config['icon'] = 'fa-flash'
                session_config['color'] = 'orange'
            elif 'ok' in head_flag:
                print 'IN OVERALL STATUS'
                session_config['icon'] = 'fa-check'
                session_config['color'] = 'green'
                session_config['final'] = 'collapse'

            # update database
            session.write_session_config(session_config)
            session.write_session_config_hws(session_config_hws_ds18b20)
            session.close()
            # render template
            return render_template("index.html", name='config',
                                   version=__version__,
                                   ds18b20_vars=session_config_hws_ds18b20,
                                   ds18b20_table=ds18b20_table,
                                   session_config=session_config,
                                   navbar_status=navbar_status,
                                   session_icon=session_icon,
                                   session_color=session_color,
                                   session_name=session_name)
        elif 'software' in request.form:
            print 'software button'

            for key in ds18b20_table.keys():
                print key, request.form[key]

            duration = int(request.form['duration'])
            interval = int(request.form['interval'])
            session.write_session_config_sws(duration, interval)
            # close session
            session.close()
            return render_template("index.html", name='monitor',
                                   version=__version__)
    else:
        session_config = session.get_session_config()
        print session_config
        session_config_hws_ds18b20 = session.get_session_config_hws()

        # duration, interval = session.get_session_config_sws()

        # check if dsb18 table exist and react
        ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
        if ds18b20_table_check:
            ds18b20_table = session.get_sensor_info('SENSOR_IDS_DS18B20')

        session.close()
        return render_template("index.html", name='config', version=__version__,
                               ds18b20_vars=session_config_hws_ds18b20,
                               ds18b20_table=ds18b20_table,
                               session_config=session_config,
                               navbar_status=navbar_status,
                               session_icon=session_icon,
                               session_color=session_color,
                               session_name=session_name)


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
    return render_template("index.html", name='licence', version=__version__)

# host='0.0.0.0'

if __name__ == "__main__":
    app.run()
