from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required

from db import db

profile_bp = Blueprint('profile', __name__, url_prefix="/profile")

def find_user(user_id: str):
    try:
        oid = ObjectId(user_id)
    except (InvalidId, TypeError):
        abort(404)
    user = db.users.find_one({"_id": oid}, {"password": 0})
    if user is None:
        abort(404)
    return user


@profile_bp.route("/")
@login_required
def my_profile():
    user = find_user(current_user.id)
    return render_template("profile.html", user=user, is_own=True)

@profile_bp.route("/<user_id>")
def view(user_id):
    user = find_user(user_id)
    is_own = current_user.is_authenticated and current_user.id == str(user["_id"])
    return render_template("profile.html", user=user, is_own=is_own)

@profile_bp.route("/edit")
@login_required
def edit():
    # still working on rn
    user = find_user(current_user.id)
    return render_template("editProfile.html", user=user)
