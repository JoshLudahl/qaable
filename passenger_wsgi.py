from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    other=request.args.get("name", "world")
    resp = make_response(render_template('index.html', name=other), 200)
    resp.headers['X-Someting'] = 'Great'
    return resp
application = app
