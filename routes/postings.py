import re
from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

postings_bp = Blueprint("postings", __name__, url_prefix="/postings")

@postings_bp.route("/")
@login_required
def posts():
    search = request.args.get("skill", "").strip()

    query = {
        "_id": {"$ne": ObjectId(current_user.id)},
        "teach_skills.0": {"$exists": True},
    }

    # If they searched, only keep users whose teach_skills contain that text (case-insensitive)
    if search:
        query["teach_skills"] = {"$regex": re.escape(search), "$options": "i"}

    # Get matching users from the database, only their username and  skills but never passwords 
    users = list(db.users.find(query, {"username": 1, "teach_skills": 1}).sort("username", 1))

    # Every skill anyone teaches, for the "Browse by skill" links
    all_skills = sorted(db.users.distinct("teach_skills"), key=str.lower)

    return render_template("postings.html", users=users, search=search, all_skills=all_skills)
