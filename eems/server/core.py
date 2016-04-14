# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template
from eems import __version__


app = Flask(__name__)


@app.route("/eems/")
def index():
    return render_template("index.html", name='index', version=__version__)


@app.route("/eems/config/")
def config():
    return render_template("index.html", name='config', version=__version__)


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor', version=__version__)


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence', version=__version__)


if __name__ == "__main__":
    app.run()
