from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

postings_bp = Blueprint("postings", __name__, url_prefix="/postings")

@postings_bp.route("/")
@login_required
def posts():
    return render_template("postings.html")