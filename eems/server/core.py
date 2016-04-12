# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template


app = Flask(__name__)


@app.route("/eems/")
# @app.route('/eems/<config>/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
