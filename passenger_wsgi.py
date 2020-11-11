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
    return requests.get(base_url)

@app.route('/')
def hello_world():
    weather=getWeather().json()
    resp = make_response(render_template('index.html', weather=weather, 200)
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


