from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from db import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/matches")
def matches():
    return "<p>This is my matches page</p"