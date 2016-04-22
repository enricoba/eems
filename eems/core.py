# -*- coding: utf-8 -*-
"""
Server core module
"""

# import external modules
from flask import Flask, render_template, request

# import eems modules
from __init__ import __version__
from support import sqlite
from support import detects, checks
from sensors import ds18b20


app = Flask(__name__)
sensors_vars = {
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
}


@app.route("/eems/")
def index():
    if request.method == 'POST':
        print 'hello'
        # open/new database
    else:
        return render_template("index.html", name='index', version=__version__)


@app.route("/eems/config/", methods=['GET', 'POST'])
def config():
    global sensors_vars
    global ds18b20_vars
    global dht11_vars

    if request.method == 'POST':
        if 'hardware-next' in request.form:
            # DS18B20 sensor
            ds18b20_cb = 'ds18b20_cb' in request.form
            if ds18b20_cb is True:
                ds18b20_vars['display'] = 'true'
                sensors_vars['display'] = 'true'
                # execute check
                # c = checks.Check()
                check = True
                #if c.w1_config() is True and c.w1_modules() is True:
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
                        # ds18b20_vars['sensors'] = ds18b20.read_ds18b20(tmp_dict)
                        ds18b20_vars['sensors'] = sensors
                        ds18b20_vars['list'] = 'true'
                        ds18b20_vars['status'] = 'alert-success'
                        ds18b20_vars['msg_1'] = 'Success!'
                        ds18b20_vars['msg_2'] = ' - {} DS18B20 sensors have ' \
                                                'been detected.'.format(
                                len(ds18b20_vars['sensors']))
                        sensors_vars['status']['ds18b20'] = 'ok'
                    else:
                        ds18b20_vars['status'] = 'alert-warning'
                        ds18b20_vars['msg_1'] = 'Warning!'
                        ds18b20_vars['msg_2'] = ' - No DS18B20 sensors have been detected.'
                        sensors_vars['status']['ds18b20'] = 'war'
                else:
                    ds18b20_vars['status'] = 'alert-danger'
                    ds18b20_vars['msg_1'] = 'Error!'
                    ds18b20_vars['msg_2'] = ' - DS18B20 hardware ' \
                                            'requirements failed.'
                    sensors_vars['status']['ds18b20'] = 'error'

            # DHT11 sensor
            dht11_cb = 'dht11_cb' in request.form
            if dht11_cb is True:
                dht11_vars['display'] = 'true'
                sensors_vars['display'] = 'true'
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
                        sensors_vars['status']['dht11'] = 'ok'
                    else:
                        dht11_vars['status'] = 'alert-warning'
                        dht11_vars['msg_1'] = 'Warning!'
                        dht11_vars['msg_2'] = ' - No DHT11 sensors have been detected.'
                        sensors_vars['status']['dht11'] = 'war'
                else:
                    dht11_vars['status'] = 'alert-danger'
                    dht11_vars['msg_1'] = 'Error!'
                    dht11_vars['msg_2'] = ' - DHT11 hardware ' \
                                          'requirements failed.'
                    sensors_vars['status']['dht11'] = 'error'

            # manage overall status
            if 'error' in sensors_vars['status'].values():
                sensors_vars['icon'] = 'fa-exclamation'
                sensors_vars['color'] = 'red'
            elif 'war' in sensors_vars['status'].values():
                sensors_vars['icon'] = 'fa-flash'
                sensors_vars['color'] = 'orange'
            elif 'ok' in sensors_vars['status'].values():
                sensors_vars['icon'] = 'fa-check'
                sensors_vars['color'] = 'green'
                sensors_vars['final'] = 'collapse'

            # render template
            return render_template("index.html", name='config',
                                   version=__version__,
                                   ds18b20_vars=ds18b20_vars,
                                   dht11_vars=dht11_vars,
                                   sensors_vars=sensors_vars)
        elif 'software' in request.form:
            print 'software button'
            for key in dht11_vars['sensors'].keys():
                print key, request.form[key]
            return render_template("index.html", name='monitor',
                                   version=__version__)
    else:
        return render_template("index.html", name='config', version=__version__,
                               ds18b20_vars=ds18b20_vars, dht11_vars=dht11_vars,
                               sensors_vars=sensors_vars)


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)

# host='0.0.0.0'

if __name__ == "__main__":
    app.run()
