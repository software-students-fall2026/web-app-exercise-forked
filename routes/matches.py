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
            {"sender": user_id},
            {"receiver": user_id},
        ]
    }))
    
    return render_template("matches.html", matches=all_matches)

@matches_bp.route("/approve/<match_id>", methods=["POST"])
@login_required
def approve_match(match_id):
    try:
        match_oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)
    
    user_id = ObjectId(current_user.id)
    res = db.matches.update_one(
        {
            "_id": match_oid, 
            "$or": [
                {"sender": user_id},
                {"receiver": user_id},
            ]
        },
        {"$set": {"status": "Approved"}}
    )
    if res.matched_count == 0:
        abort(404)

    return redirect(url_for("matches.my_matches"))

@matches_bp.route("/decline/<match_id>", methods=["POST"])
@login_required
def decline_match(match_id):
    try:
        match_oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)

    user_id = ObjectId(current_user.id)
    res = db.matches.delete_one(
        {
            "_id": match_oid, 
            "$or": [
                {"sender": user_id},
                {"receiver": user_id},
            ]
        },
    )
    if res.deleted_count == 0:
        abort(404)

    return redirect(url_for("matches.my_matches"))

@matches_bp.route("/add/<user_id>", methods=["POST"])
@login_required
def add_match(user_id):
    try:
        receiver_oid = ObjectId(user_id)
    except (InvalidId, TypeError):
        abort(404)

    res = db.matches.insert_one({
        "sender": ObjectId(current_user.id),
        "receiver": receiver_oid,
        "status": "Awaiting Approval",
        "date": datetime.now(timezone.utc)
    })

    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$addToSet": {
                "sent_matches": receiver_oid
            }
        }
    )

    return "", 204