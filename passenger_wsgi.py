import json, os, requests, smtplib
from flask import Flask, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from datetime import datetime as dt
from weather_dict import WEATHER_ICONS

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


def getWeather(lat=45.445033, lon=-122.793760):
    api_key = os.environ.get("WEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lat) + "&lon=" + str(
        lon) + "&units=imperial&appid=" + api_key
    return requests.get(base_url)


def getGeoData(zip):
    try:
        req = requests.get(
            "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&q=" + str(
                zip) + "&facet=state&facet=timezone&facet=dst")
        return req
    except requests.exceptions.RequestException as e:
        return 404


def send_email():
    smtp_obj = smtplib.SMTP_SSL('qaable.com', 465)
    smtp_obj.ehlo()
    smtp_obj.login(os.environ.get("EMAIL"), os.environ.get("EMAIL_PASSWORD"))
    smtp_obj.sendmail(os.environ.get('EMAIL'), 'qa@qaable.com', 'Subject: Testing. \nLove it.')
    smtp_obj.quit()


@app.route('/')
def hello_world():
    weather = getWeather()
    return make_response(
        render_template(
            'index.html',
            weather=weather.json()
        ),
        200
    )


@app.route('/', methods=["POST"])
def postHello():
    req = request.form.get("zip", "None")
    zip = request.form.get("zip")
    if zip.isdigit() and len(zip) == 5:
        req = geo = getGeoData(req).json()
        if geo['nhits'] == 0:
            return make_response(
                render_template(
                    'index.html',
                    error='Invalid zip code.'
                ),
                200
            )

        else:
            longitude = geo['records'][0]['fields']['longitude']
            latitude = geo['records'][0]['fields']['latitude']
            city = geo['records'][0]['fields']['city']
            state = geo['records'][0]['fields']['state']
            weather = getWeather(latitude, longitude)
            return make_response(
                render_template(
                    'index.html',
                    weather=weather.json(),
                    city=city,
                    state=state
                ),
                200
            )

    else:
        return make_response(
            render_template(
                'index.html',
                error='Invalid zip code.'
            ),
            200
        )


# filter for formatting timestamp to day of the week, ie Monday, Tuesday, etc.
@app.template_filter('datetimeformat')
def datetimeformat(value, offset):
    return dt.fromtimestamp(value + offset).strftime("%A")


@app.template_filter('weather_icon_filter')
def weather_icon_filter(value, icon_value):
    value = str(value)
    icon_value = icon_value[2:]
    if icon_value == "d":
        value = value + icon_value

    return WEATHER_ICONS[value]


application = app
