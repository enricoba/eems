# -*- coding: utf-8 -*-
"""
Server core module
"""


from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
@app.route('/<name>')
def homepage(name=None):
    return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run()
