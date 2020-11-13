import os
import smtplib
from flask import Flask, request, render_template, make_response, redirect, session, url_for
from flask_session import Session
from datetime import datetime as dt
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
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat=45.445033&lon=-122.793760&units=imperial&appid=" + api_key
    return requests.get(base_url)

def send_email():
    smtpObj = smtplib.SMTP_SSL('qaable.com', 465)
    smtpObj.ehlo()
    smtpObj.login(os.environ.get("EMAIL"), os.environ.get("EMAIL_PASSWORD"))
    smtpObj.sendmail(os.environ.get("EMAIL", 'qa@qaable.com', 'Subject: Testing. \nLove it.'))
    smtpObj.quit()

@app.route('/')
def hello_world():
    weather=getWeather()
    send_email()
    return  make_response(
        render_template(
            'index.html', 
            weather=weather.json()
        ), 
        200
    )

@app.route('/', methods = ["POST"])
def postHello():
    session["name"] = request.form.get("name")
    req = request.form.get("name", "world")
    weather = getWeather()
    return make_response(
        render_template(
            'index.html', 
            named=req, 
            weather=weather.json()
        ), 
        200
    )
@app.template_filter('datetimeformat')
def datetimeformat(value, offset):
    return dt.fromtimestamp(value - offset).strftime("%A")

application = app
