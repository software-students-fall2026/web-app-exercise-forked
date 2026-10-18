from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
load_dotenv()
import os
from db import db
from routes.auth import auth_bp, login_manager
from routes.profile import profile_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)