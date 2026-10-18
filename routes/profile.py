from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required

from db import db

profile_bp = Blueprint('profile', __name__, url_prefix="/profile")

@profile_bp.route("/")
@login_required
def my_profile():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})
    return render_template("myProfile.html", user=user)

@profile_bp.route("/<user_id>")
def view(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        abort(404)

    return render_template("profile/view.html", user=user)
