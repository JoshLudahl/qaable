import os
from flask import Flask, request, render_template, make_response, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

Session(app)

import test

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    req=request.args.get("name", "world")
    resp = make_response(render_template('index.html', name=req), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

@app.route('/', methods = ["POST"])
def postHello():
    unit = os.environ.get("UNIT")
    
    session["name"] = request.form.get("name", None)
    req = request.form.get("name", "world")
    resp = make_response(render_template('index.html', name=req, unit=unit), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

application = app
