from flask import Flask, render_template
from jinja2.ext import Extension

from utils import ext

static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)

for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    app.jinja_env.add_extension(extension)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/login/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signUp")
def signUp():
    return render_template('signUp.html')
