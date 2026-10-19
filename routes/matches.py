from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

matches_bp = Blueprint("matches", __name__, url_prefix="/matches")

@matches_bp.route("/")
@login_required
def my_matches():
    matches = db["matches"]
    return render_template("matches.html")