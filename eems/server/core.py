# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template, request
# from OpenSSL import SSL
from eems import __version__


# context = SSL.Context(SSL.TLSv1_1_METHOD)
# context.set_options(SSL.OP_NO_SSLv2)


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
        print 'POST  method'
    else:
        success = 'display: none'
        print 'GET / else method'
    return render_template("index.html", name='config', version=__version__,
                           success=success)


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)


if __name__ == "__main__":
    app.run()
