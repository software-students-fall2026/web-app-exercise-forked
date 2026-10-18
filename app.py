from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
load_dotenv()
from db import db
from routes.auth import auth_bp, login_manager

app = Flask(__name__)
app.secret_key = 'secretkeyforflasklogin'

login_manager.init_app(app)
app.register_blueprint(auth_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/matches")
def matches():
    return "<p>This is my matches page</p"

if __name__ == "__main__":
    app.run(debug=True)