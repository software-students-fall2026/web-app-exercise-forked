from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from db import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/myProfile")
def myProfile():
    return render_template("myProfile.html")

@app.route("/theirProfile")
def theirProfile():
    return render_template("theirProfile.html")

@app.route("/editProfile")
def editProfile():
    return render_template("editProfile.html")

@app.route("/matches")
def matches():
    return render_template("matches.html")

@app.route("/map")
def map():
    return render_template("map.html")