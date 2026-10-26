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


@matches_bp.route("/rate/<match_id>", methods=["POST"])
@login_required
def rate_match(match_id):
    try:
        match_oid = ObjectId(match_id)
    except (InvalidId, TypeError):
        abort(404)
    
    user_oid = ObjectId(current_user.id)
    match = db.matches.find_one(
        {
            "_id": match_oid, 
            "$or": [
                {"sender": user_oid},
                {"receiver": user_oid},
            ]
        },
    )
    if match is None:
        abort(404)

    if match["sender"] == user_oid:
        rating_field = "sender_rating"
    else:
        rating_field = "receiver_rating"

    rating = request.form.get("rating", type=int)
    if rating is None or not 1 <= rating <= 5:
        abort(400)
        
    res = db.matches.update_one(
        {
            "_id": match_oid,
            "$or": [
                {"sender" : user_oid},
                {"receiver": user_oid}
            ]
        },
        {"$set": {rating_field : rating}}
    )

    if res.matched_count == 0:
        abort(404)

    if match["sender"] == user_oid:
        rated_oid = match["receiver"]
    else:
        rated_oid = match["sender"]

    rated_matches = db.matches.find(
        {
            "$or": [
                {"sender": rated_oid},
                {"receiver": rated_oid}
            ]
        },
        {
            "sender": 1,
            "sender_rating": 1,
            "receiver_rating": 1
        }
    )

    total = 0
    rating_count = 0

    for rated_match in rated_matches:
        if rated_match["sender"] == rated_oid:
            score = rated_match.get("receiver_rating")
        else:
            score = rated_match.get("sender_rating")

        if score is not None:
            total += score
            rating_count += 1

    average_rating = (round(total / rating_count, 1) if rating_count else None)

    db.users.update_one(
        {"_id": rated_oid},
        {
            "$set": {
                "average_rating": average_rating,
                "rating_count": rating_count
            }
        }
    )

    return redirect(url_for("matches.my_matches"))