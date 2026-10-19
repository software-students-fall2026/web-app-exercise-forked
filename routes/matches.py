from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

matches_bp = Blueprint("matches", __name__, url_prefix="/matches")

@matches_bp.route("/")
@login_required
def my_matches():
    all_matches = list(db.matches.find({"user_one": ObjectId(current_user.id)}))
    return render_template("matches.html", matches=all_matches)

@matches_bp.route("/approve/<match_id>", methods=["POST"])
@login_required
def approve_match():
    try:
        oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)
    
    res = db.matches.update_one(
        {"_id": oid, "user_one": ObjectId(current_user.id)},
        {"$set": {"approved": True}}
    )
    if res.matched_count == 0:
        abort(404)

    return redirect(urlfor(matches.my_matches))

@matches_bp.route("/decline/<match_id>", methods=["POST"])
@login_required
def decline_match():
    try:
        oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)
    
    res = db.matches.deleteOne(
        {"_id": oid, "user_one": ObjectId(current_user.id)}
    )
    if res.deleted_count == 0:
        abort(404)

    return redirect(urlfor(matches.my_matches))