from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

postings_bp = Blueprint("postings", __name__, url_prefix="/postings")

def read_age(name):
    value = request.args.get(name, "").strip()
    if value.isdigit():
        return int(value)
    return None

@postings_bp.route("/")
@login_required
def posts():
    search = request.args.get("skill", "").strip()
    min_age = read_age("min_age")
    max_age = read_age("max_age")

    if min_age is not None and max_age is not None:
        min_age, max_age = min(min_age, max_age), max(min_age, max_age)

    current_user_id = ObjectId(current_user.id)
    cur_user = db.users.find_one({"_id": current_user_id})
    sent_matches = cur_user.get("sent_matches", [])

    user_location = cur_user.get("location")
    local_count = db.users.count_documents({"location": user_location}) if user_location else 0

    query = {
        "_id": {
            "$nin": sent_matches + [current_user_id]
        },
        "teach_skills.0": {"$exists": True},
    }

    age_filter = {}
    if min_age is not None:
        age_filter["$gte"] = min_age
    if max_age is not None:
        age_filter["$lte"] = max_age
    if age_filter:
        query["age"] = age_filter


    # If they searched, only keep users with a teach skill name containing that text (case-insensitive)
    if search:
        query["teach_skills.name"] = {"$regex": re.escape(search), "$options": "i"}

    # Get matching users from the database, only their username and  skills but never passwords 
    users = list(db.users.find(query, {"username": 1, "teach_skills": 1}).sort("username", 1))

    # Every skill anyone teaches, for the "Browse by skill" links
    all_skills = sorted(db.users.distinct("teach_skills.name"), key=str.lower)

    return render_template(
        "postings.html", 
        users=users, 
        search=search, 
        all_skills=all_skills, 
        min_age=min_age, 
        max_age=max_age, 
        local_count = local_count,
        user_location = user_location
    )