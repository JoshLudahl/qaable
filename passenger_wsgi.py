import os
from flask import Flask, request, render_template, make_response, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config.update(
    SESSION_PERMANENT=False,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)

Session(app)

import test

@app.route('/')
@app.route('/<name>')
def hello_world():
    req=request.args.get("name", "world")
    resp = make_response(render_template('index.html', name=req), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

@app.route('/', methods = ["POST"])
def postHello():
    unit = os.environ.get("UNIT")
    session["name"] = request.form.get("name")
    req = request.form.get("name", "world")
    resp = make_response(render_template('index.html', named=req, unit=unit), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

application = app
