from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

matches_bp = Blueprint("matches", __name__, url_prefix="/matches")

@matches_bp.route("/")
@login_required
def my_matches():
    user_id = ObjectId(current_user.id)
    all_matches = list(db.matches.find({
        "$or": [
            {"user_one": user_id},
            {"user_two": user_id},
        ]
    }))
    return render_template("matches.html", matches=all_matches)

@matches_bp.route("/approve/<match_id>", methods=["POST"])
@login_required
def approve_match():
    try:
        oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)
    
    user_id = ObjectId(current_user.id)
    res = db.matches.update_one(
        {
            "_id": oid, 
            "$or": [
                {"user_one": user_id},
                {"user_two": user_id},
            ]
        },
        {"$set": {"status": "Approved"}}
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

    user_id = ObjectId(current_user.id)
    res = db.matches.deleteOne(
        {
            "_id": oid, 
            "$or": [
                {"user_one": user_id},
                {"user_two": user_id},
            ]
        },
    )
    if res.deleted_count == 0:
        abort(404)

    return redirect(urlfor(matches.my_matches))

@matches_bp.route("/matches/add/<user_id>")
@login_required
def add_match():
    try:
        oid = ObjectId(user_id)
    except (InvalidId, TypeError):
        abort(404)
    
    res = db.matches.insert_one({
        "user_one": ObjectId(current_user.id),
        "user_two": oid,
        "status": "Awaiting",
        "date": datetime.now(timezone.utc)
    })

    return "", 204