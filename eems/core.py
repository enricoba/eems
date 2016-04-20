# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template, request
from eems.support import detects, checks
from eems import __version__


app = Flask(__name__)


@app.route("/eems/")
def index():
    return render_template("index.html", name='index', version=__version__)


@app.route("/eems/config/", methods=['GET', 'POST'])
def config():
    ds18b20_vars = {
        'display': 'display: none',
        'list': 'display: none',
        'status': '',
        'msg_1': '',
        'msg_2': '',
        'sensors': []
    }
    dht11_vars = {
        'display': 'display: none',
        'list': 'display: none',
        'status': '',
        'msg_1': '',
        'msg_2': '',
        'sensors': []
    }
    if request.method == 'POST':
        ds18b20_cb = 'ds18b20_cb' in request.form
        if ds18b20_cb is True:
            ds18b20_vars['display'] = 'display: true'
            # execute check
            c = checks.Check()
            # check = True
            if c.w1_config() is True and c.w1_modules() is True:
            # if check is True:
                # check sensors
                # ds18b20_vars['sensors'] = ['1', '2', '3', '4']
                ds18b20_vars['sensors'] = detects.ds18b20_sensors()
                if len(ds18b20_vars['sensors']):
                    ds18b20_vars['list'] = 'display: true'
                    ds18b20_vars['status'] = 'alert-success'
                    ds18b20_vars['msg_1'] = 'Success!'
                    ds18b20_vars['msg_2'] = ' - {} sensors have ' \
                                            'been detected.'.format(
                            len(ds18b20_vars['sensors']))
                else:
                    ds18b20_vars['status'] = 'alert-warning'
                    ds18b20_vars['msg_1'] = 'Warning!'
                    ds18b20_vars['msg_2'] = ' - No sensors have been detected.'
            else:
                ds18b20_vars['status'] = 'alert-danger'
                ds18b20_vars['msg_1'] = 'Error!'
                ds18b20_vars['msg_2'] = ' - DS18B20 hardware ' \
                                        'requirements failed.'

    return render_template("index.html", name='config', version=__version__,
                           ds18b20_vars=ds18b20_vars, dht11_vars=dht11_vars)


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
