# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template


app = Flask(__name__)


@app.route("/eems/")
def index():
    return render_template("index.html", name='index')


@app.route("/eems/config/")
def config():
    return render_template("index.html", name='config')


@app.route("/eems/monitor/")
def monitor():
    return render_template("index.html", name='monitor')


@app.route("/eems/licence/")
def licence():
    return render_template("index.html", name='licence')


if __name__ == "__main__":
    app.run()
