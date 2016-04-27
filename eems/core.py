# -*- coding: utf-8 -*-
"""
Server core module
"""

# import external modules
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from shutil import copyfile


# import eems modules
from __init__ import __version__
from support import sqlite
# from support import detects, checks
# from sensors import ds18b20


# get saved profiles
# tmp = os.listdir("D:\F_Projects\F-I_GitHub\eems\eems\data")
tmp = os.listdir('/Volumes/Tesla/05_Github/eems/eems/data')
profiles = ['new']
for i in tmp:
    if i != 'default.db':
        profiles.append(i[:-3])


profile = None
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    # get session object
    global profiles
    global profile

    if request.method == 'POST':
        profile_tmp = request.form['session-input']
        if len(profile_tmp):
            profiles.append(str(profile_tmp))
            profile = profile_tmp
            print profile

            # add default tables and contents
            """
            subprocess.call(['cp', '/home/pi/eems/default.db',
                             '/home/pi/eems/{}.db'.format(profile)])

            copyfile('D:/F_Projects/F-I_GitHub/eems/eems/data/default.db',
                     'D:/F_Projects/F-I_GitHub/eems/eems/data/{}.db'.format(profile))
            """
            subprocess.call(['cp', '/Volumes/Tesla/05_Github/eems/eems/data/default.db',
                             '/Volumes/Tesla/05_Github/eems/eems/data/{}.db'.format(profile)])
            # redirect
            return redirect(url_for('config'))
        else:
            # todo profile laden
            print 'load project'
            profile = request.form['session-load']
            return redirect(url_for('config'))
    else:
        print profiles
        return render_template("index.html", name='index', version=__version__,
                               profiles=profiles, len=len(profiles))


@app.route("/config/", methods=['GET', 'POST'])
def config():
    # get session object
    # global ds18b20_vars
    # global dht11_vars
    global profile
    session = sqlite.DBHandler()
    session.start(profile)
    ds18b20_table = {}
    dht11_table = {}
    if request.method == 'POST':
        session_config = session.get_session_config()
        ds18b20_vars, dht11_vars = session.get_session_config_hws()
        print 'POST: ', session_config
        if 'hardware-next' in request.form:
            head_flag = list()
            # DS18B20 sensor
            ds18b20_cb = 'ds18b20_cb' in request.form
            if ds18b20_cb is True:
                ds18b20_vars['display'] = 'true'
                session_config['display'] = 'true'
                # execute check
                # c = checks.Check()
                check = True
                # if c.w1_config() is True and c.w1_modules() is True:
                if check is True:
                    # check sensors
                    sensors = ['1', '2', 'adsad']
                    # sensors = detects.ds18b20_sensors()
                    if len(sensors):
                        # add sensor_ids_table
                        # warum nicht gleich mit werten?
                        # verschieben hinter Zeile 108 bzw. 111
                        session.add_sensor_ids_table('ds18b20')
                        session.add_sensor_ids('ds18b20', sensors)
                        print 'nach schreiben SQL'
                        # read temperatures
                        tmp_dict = dict()
                        for sensor in sensors:
                            tmp_dict[sensor] = 20
                        # ds18b20_vars['sensors'] = ds18b20.read_
                        # ds18b20(tmp_dict)
                        print 'tmp_dict: ', tmp_dict
                        # ds18b20_vars['sensors'] = tmp_dict
                        ds18b20_table = tmp_dict
                        ds18b20_vars['list'] = 'true'
                        ds18b20_vars['status'] = 'alert-success'
                        ds18b20_vars['msg_1'] = 'Success!'
                        ds18b20_vars['msg_2'] = ' - {} DS18B20 sensors have ' \
                                                'been detected.'.format(
                                len(ds18b20_table))
                        head_flag.append('ok')
                        print 'ende ds18b20 block'
                    else:
                        ds18b20_vars['status'] = 'alert-warning'
                        ds18b20_vars['msg_1'] = 'Warning!'
                        ds18b20_vars['msg_2'] = ' - No DS18B20 sensors have ' \
                                                'been detected.'
                        head_flag.append('war')
                else:
                    ds18b20_vars['status'] = 'alert-danger'
                    ds18b20_vars['msg_1'] = 'Error!'
                    ds18b20_vars['msg_2'] = ' - DS18B20 hardware ' \
                                            'requirements failed.'
                    head_flag.append('error')

            # DHT11 sensor
            dht11_cb = 'dht11_cb' in request.form
            if dht11_cb is True:
                dht11_vars['display'] = 'true'
                session_config['display'] = 'true'
                # execute check
                check = True
                if check is True:
                    # check sensors
                    sensors = {
                        'DHT11-1': 12,
                        'DHT11-2': 14,
                        'DHT11-3': 50,
                        'DHT11-4': 70
                    }
                    if len(sensors):
                        dht11_vars['sensors'] = sensors
                        dht11_vars['list'] = 'true'
                        dht11_vars['status'] = 'alert-success'
                        dht11_vars['msg_1'] = 'Success!'
                        dht11_vars['msg_2'] = ' - {} DHT11 sensors have ' \
                                              'been detected.'.format(
                                len(dht11_vars['sensors']))
                        dht11_vars['status'] = 'ok'
                    else:
                        dht11_vars['status'] = 'alert-warning'
                        dht11_vars['msg_1'] = 'Warning!'
                        dht11_vars['msg_2'] = ' - No DHT11 sensors have ' \
                                              'been detected.'
                        dht11_vars['status'] = 'war'
                else:
                    dht11_vars['status'] = 'alert-danger'
                    dht11_vars['msg_1'] = 'Error!'
                    dht11_vars['msg_2'] = ' - DHT11 hardware ' \
                                          'requirements failed.'
                    dht11_vars['status'] = 'error'

            print 'vor overall status'
            print dht11_vars['status']
            print ds18b20_vars['status']

            # manage overall status
            if 'error' in head_flag:
                session_config['icon'] = 'fa-exclamation'
                session_config['color'] = 'red'
            elif 'war' in head_flag:
                session_config['icon'] = 'fa-flash'
                session_config['color'] = 'orange'
            elif 'ok' in head_flag:
                session_config['icon'] = 'fa-check'
                session_config['color'] = 'green'
                session_config['final'] = 'collapse'

            # update database
            print 'vor schreiben: ', session_config
            session.write_session_config(session_config)
            print 'vor config hws '
            session.write_session_config_hws(ds18b20_vars, dht11_vars)
            session.close()
            print 'vor return template'
            # render template
            return render_template("index.html", name='config',
                                   version=__version__,
                                   ds18b20_vars=ds18b20_vars,
                                   ds18b20_table=ds18b20_table,
                                   dht11_table=dht11_table,
                                   dht11_vars=dht11_vars,
                                   session_config=session_config)
        elif 'software' in request.form:
            print 'software button'
            """
            for key in dht11_vars['sensors'].keys():
                print key, request.form[key]
            """
            duration = int(request.form['duration'])
            print 'duration', duration, type(duration)
            interval = int(request.form['interval'])
            print 'interval', interval, type(interval)
            session.write_session_config_sws(duration, interval)
            # close session
            session.close()
            print 'session close, vor render template'
            return render_template("index.html", name='monitor',
                                   version=__version__)
    else:
        session_config = session.get_session_config()
        ds18b20_vars, dht11_vars = session.get_session_config_hws()

        # duration, interval = session.get_session_config_sws()

        # check if dsb18/dht11 tables exist and react
        ds18b20_table_check = session.check_table_exist('SENSOR_IDS_DS18B20')
        dht11_table_check = session.check_table_exist('SENSOR_IDS_DHT11')

        session.close()

        """if ds18b20_table_check is True:
            ds18b20_table = """

        print 'GET: ', session_config
        print 'GET: ', ds18b20_vars
        print 'GET: ', dht11_vars
        return render_template("index.html", name='config', version=__version__,
                               ds18b20_vars=ds18b20_vars,
                               ds18b20_table=ds18b20_table,
                               dht11_table=dht11_table,
                               dht11_vars=dht11_vars,
                               session_config=session_config)


@app.route("/monitor/")
def monitor():
    print 'monitor called'
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)

# host='0.0.0.0'

if __name__ == "__main__":
    app.run()
