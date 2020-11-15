import os, smtplib, requests
from flask import Flask, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from datetime import datetime as dt

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

def getWeather(lat = 45.445033, lon = -122.793760):
    api_key = os.environ.get("WEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lat) + "&lon=" + str(lon) + "&units=imperial&appid=" + api_key
    return requests.get(base_url)
    
def getGeoData(zip):
    return requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&q=" + str(zip) +"&facet=state&facet=timezone&facet=dst")

def send_email():
    smtpObj = smtplib.SMTP_SSL('qaable.com', 465)
    smtpObj.ehlo()
    smtpObj.login(os.environ.get("EMAIL"), os.environ.get("EMAIL_PASSWORD"))
    smtpObj.sendmail(os.environ.get('EMAIL'), 'qa@qaable.com', 'Subject: Testing. \nLove it.')
    smtpObj.quit()

@app.route('/')
def hello_world():
    weather=getWeather()
    return  make_response(
        render_template(
            'index.html', 
            weather=weather.json()
        ), 
        200
    )

@app.route('/', methods = ["POST"])
def postHello():
    req = request.form.get("zip","None")
    geo = getGeoData(req)
    data = geo.json()
    n = data.nhits
    weather = getWeather()
    return make_response(
        render_template(
            'index.html', 
            weather=weather.json(),
            geo=n
        ), 
        200
    )

# filter for formatting timestamp to day of the week, ie Monday, Tuesday, etc.
@app.template_filter('datetimeformat')
def datetimeformat(value, offset):
    return dt.fromtimestamp(value + offset).strftime("%A")

application = app
