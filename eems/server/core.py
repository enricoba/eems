# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template, request
from eems import __version__


app = Flask(__name__)


@app.route("/eems/")
def index():
    return render_template("index.html", name='index', version=__version__)


@app.route("/eems/config/", methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        c_1 = 'c_1' in request.form
        c_2 = 'c_2' in request.form
        print 'c_1: ', c_1
        print 'c_2: ', c_2
        if c_1 is True and c_2 is True:
            success = 'display: true'
            print 'success'
        else:
            success = 'display: none'
            print 'no success'

        if c_1 is True:
            c_1_success = 'display: true'
        else:
            c_1_success = 'display: none'
        if c_2 is True:
            c_2_success = 'display: true'
        else:
            c_2_success = 'display: none'

        print 'POST  method'
    else:
        success = 'display: none'
        c_1_success = 'display: none'
        c_2_success = 'display: none'
        print 'GET / else method'
    return render_template("index.html", name='config', version=__version__,
                           success=success, c_1_success=c_1_success,
                           c_2_success=c_2_success)


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)


if __name__ == "__main__":
    app.run()
