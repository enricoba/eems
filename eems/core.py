# -*- coding: utf-8 -*-
"""
Server core module
"""

# import external modules
import os
from flask import Flask, render_template, request, redirect, url_for


# import eems modules
from __init__ import __version__
from support import sqlite
# from support import detects, checks
# from sensors import ds18b20


# get saved profiles
tmp = os.listdir("D:\F_Projects\F-I_GitHub\eems\eems\data")
profiles = ['new']
for i in tmp:
    if i != 'default.db':
        profiles.append(i[:-3])


profile = None
app = Flask(__name__)


"""sensors_vars = {
    # head ( symbol oben)
    'display': 'none',
    'icon': 'fa-check',
    'color': 'green',
    'status': {'ds18b20': '',
               'dht11': ''},
    'final': 'deactivate'
}

ds18b20_vars = {
    'display': 'none',
    'list': 'none',
    'status': '',
    'msg_1': '',
    'msg_2': '',
    'sensors': dict()
}

dht11_vars = {
    'display': 'none',
    'list': 'none',
    'status': '',
    'msg_1': '',
    'msg_2': '',
    'sensors': dict()
}"""


@app.route("/", methods=['GET', 'POST'])
def index():
    # get session object
    global profiles
    global profile

    if request.method == 'POST':
        profile = request.form['session-input']
        if len(profile):
            profiles.append(str(profile))

            session = sqlite.DBHandler()
            session.start(profile)
            # add default tables and contents
            session.close()

            # redirect
            return redirect(url_for('config'))
        else:
            # todo profile laden
            print 'load project'
            profile = request.form['session-load']
            # session = sqlite.DBHandler()
            # session.start(profile)
            return redirect(url_for('monitor'))
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

    if request.method == 'POST':
        session_config = session.get_session_config()
        ds18b20_vars, dht11_vars = session.get_session_config_hws()
        print 'POST: ', session_config
        if 'hardware-next' in request.form:
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
                    sensors = {
                        '1': 19,
                        '2': 21,
                        '3': 50,
                        '4': 110
                    }
                    # sensors = detects.ds18b20_sensors()
                    if len(sensors):
                        # read temperatures
                        tmp_dict = dict()
                        for sensor in sensors:
                            tmp_dict[sensor] = None
                        # ds18b20_vars['sensors'] = ds18b20.read_
                        # ds18b20(tmp_dict)
                        ds18b20_vars['sensors'] = sensors
                        ds18b20_vars['list'] = 'true'
                        ds18b20_vars['status'] = 'alert-success'
                        ds18b20_vars['msg_1'] = 'Success!'
                        ds18b20_vars['msg_2'] = ' - {} DS18B20 sensors have ' \
                                                'been detected.'.format(
                                len(ds18b20_vars['sensors']))
                        ds18b20_vars['status'] = 'ok'
                    else:
                        ds18b20_vars['status'] = 'alert-warning'
                        ds18b20_vars['msg_1'] = 'Warning!'
                        ds18b20_vars['msg_2'] = ' - No DS18B20 sensors have ' \
                                                'been detected.'
                        ds18b20_vars['status'] = 'war'
                else:
                    ds18b20_vars['status'] = 'alert-danger'
                    ds18b20_vars['msg_1'] = 'Error!'
                    ds18b20_vars['msg_2'] = ' - DS18B20 hardware ' \
                                            'requirements failed.'
                    ds18b20_vars['status'] = 'error'

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

            # manage overall status
            if 'error' in dht11_vars['status'] \
                    or 'error' in ds18b20_vars['status']:
                session_config['icon'] = 'fa-exclamation'
                session_config['color'] = 'red'
            elif 'war' in dht11_vars['status'] \
                    or 'war' in ds18b20_vars['status']:
                session_config['icon'] = 'fa-flash'
                session_config['color'] = 'orange'
            elif 'ok' in dht11_vars['status'] \
                    or 'ok' in ds18b20_vars['status']:
                session_config['icon'] = 'fa-check'
                session_config['color'] = 'green'
                session_config['final'] = 'collapse'

            # update database
            print 'vor schreiben: ', session_config
            session.write_session_config(session_config)
            session.write_session_config_hws(ds18b20_vars, dht11_vars)
            session.close()

            # render template
            return render_template("index.html", name='config',
                                   version=__version__,
                                   ds18b20_vars=ds18b20_vars,
                                   dht11_vars=dht11_vars,
                                   session_config=session_config)
        elif 'software' in request.form:
            print 'software button'
            for key in dht11_vars['sensors'].keys():
                print key, request.form[key]

            # close session
            session.close()
            return render_template("index.html", name='monitor',
                                   version=__version__)
    else:
        session_config = session.get_session_config()
        ds18b20_vars, dht11_vars = session.get_session_config_hws()
        session.close()
        print 'GET: ', session_config
        return render_template("index.html", name='config', version=__version__,
                               ds18b20_vars=ds18b20_vars, dht11_vars=dht11_vars,
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
