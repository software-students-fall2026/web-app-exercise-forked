from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from db import db
from routes.profile import profile_bp

app = Flask(__name__)
app.register_blueprint(profile_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/matches")
def matches():
    return "<p>This is my matches page</p"