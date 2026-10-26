from bson.errors import InvalidId
from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

banned_bp = Blueprint("banned", __name__, url_prefix="/banned")

@banned_bp.route("/")
@login_required
def banned():
    if current_user.role != "Banned":
        return redirect(url_for("profile.my_profile"))

    return render_template("banned.html")