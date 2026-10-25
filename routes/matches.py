from bson.errors import InvalidId
from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

matches_bp = Blueprint("matches", __name__, url_prefix="/matches")

@matches_bp.route("/")
@login_required
def my_matches():
    user_oid = ObjectId(current_user.id)
    all_matches = list(db.matches.find({
        "$or": [
            {"sender": user_oid},
            {"receiver": user_oid},
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
    
    user_oid = ObjectId(current_user.id)
    res = db.matches.update_one(
        {
            "_id": match_oid, 
            "$or": [
                {"sender": user_oid},
                {"receiver": user_oid},
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

    user_oid = ObjectId(current_user.id)
    res = db.matches.delete_one(
        {
            "_id": match_oid, 
            "$or": [
                {"sender": user_oid},
                {"receiver": user_oid},
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

    sender_oid = ObjectId(current_user.id)
    sender = db.users.find_one({
        "_id": sender_oid
    })
    receiver = db.users.find_one({
        "_id": receiver_oid
    })

    res = db.matches.insert_one({
        "sender": sender_oid,
        "receiver": receiver_oid,
        "sender_name": sender["username"],
        "receiver_name": receiver["username"],
        "status": "Awaiting Approval",
        "date": datetime.now(timezone.utc)
    })

    db.users.update_one(
        {"_id": sender_oid},
        {
            "$addToSet": {
                "sent_matches": receiver_oid
            }
        }
    )

    return "", 204