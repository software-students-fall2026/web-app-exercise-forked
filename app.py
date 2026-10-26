from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from dotenv import load_dotenv
load_dotenv()
import os
from routes.auth import auth_bp, login_manager
from routes.profile import profile_bp
from routes.matches import matches_bp
from routes.postings import postings_bp
from routes.dms import dms_bp
from socket_event import socketio
from routes.moderation import moderation_bp
from routes.banned import banned_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(matches_bp)
app.register_blueprint(postings_bp)
app.register_blueprint(dms_bp)
app.register_blueprint(banned_bp)
socketio.init_app(app)

app.register_blueprint(moderation_bp)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("profile.my_profile")) 

    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)