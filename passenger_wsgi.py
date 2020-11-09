from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    req=request.args.get("name", "world")
    resp = make_response(render_template('index.html', name=req), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

@app.route('/', methods = ["POST"])
def postHello():
    req = request.form.get("name", "world")
    resp = make_response(render_template('index.html', name=req), 200)
    resp.headers['X-Something'] = 'Custom'
    return resp

application = app
