import os
from flask import Flask, request, render_template, make_response, redirect, session, url_for
from flask_session import Session
import requests

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

def getWeather():
    api_key = os.environ.get("WEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat=45.4187&lon=122.7872&units=imperial&appid=" + api_key
    req = requests.get(base_url)
    print(req)
    return req

@app.route('/')
@app.route('/<name>')
def hello_world():
    req=request.args.get("name", "world")
    weather=getWeather()
    resp = make_response(render_template('index.html', name=req, weather=weather), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

@app.route('/', methods = ["POST"])
def postHello():
    unit = os.environ.get("UNIT")
    session["name"] = request.form.get("name")
    req = request.form.get("name", "world")
    weather = getWeather()
    resp = make_response(render_template('index.html', named=req, unit=unit, weather=weather.json()), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

application = app


