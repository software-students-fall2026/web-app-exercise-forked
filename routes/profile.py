from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db
from .auth import validate_phone

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

PROFICIENCY_LEVELS = ["No Experience", "Beginner", "Intermediate", "Advanced", "Expert"]
BLANK_ROWS = 2 

def read_skills(prefix, old_skills):
    """Rebuild skill list from the form rows named <prefix>_name, <prefix>_proficiency, <prefix>_description."""
    old_images = {s["name"].lower(): s.get("images", []) for s in old_skills if isinstance(s, dict)}
    names = request.form.getlist(f"{prefix}_name")
    levels = request.form.getlist(f"{prefix}_proficiency")
    descriptions = request.form.getlist(f"{prefix}_description")

    skills, seen = [], set()
    for name, level, description in zip(names, levels, descriptions):
        name = name.strip().title()

        if not name or name.lower() in seen: 
            continue
        seen.add(name.lower())

        skills.append({
            "name": name,
            "proficiency": level if level in PROFICIENCY_LEVELS else "",
            "description": description.strip(),
            "images": old_images.get(name.lower(), []),
        })
    return skills

@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    user = find_user(current_user.id)
    teach_skills = user.get("teach_skills", [])
    learn_skills = user.get("learn_skills", [])

    def show_form(error=None):
        return render_template("editProfile.html", user=user, levels=PROFICIENCY_LEVELS, blank_rows=BLANK_ROWS, error=error)

    if request.method == "GET":
        return show_form()

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    age_text = request.form.get("age", "").strip()
    phone = request.form.get("phone", "").strip()

    if not username:
        return show_form("Username can't be empty.")

    
    if email != user.get('email') and db.users.find_one({'email': email}):
        return show_form('Email already registered, please pick another') 
    
    if username != user.get('username') and db.users.find_one({'username': username}):
        return show_form('Username already registered, please pick another') 

    if phone and phone != user.get('phone') and db.users.find_one({'phone': phone}):       # phone is there so you can remove your number. if it's empty it allows it to happen instead
        return show_form('Phone number already registered')                                # of triggering either of the forms

    if phone and validate_phone(phone) == False:
        return show_form('Please enter a valid phone number') 

    age = None
    if age_text:
        if not age_text.isdigit() or not 1 <= int(age_text) <= 120:
            return show_form("Age must be a whole number from 1 to 120.")
        age = int(age_text)

    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "username": username,
            "email": email,
            "age": age,
            "phone": phone,
            "teach_skills": read_skills("teach", teach_skills),
            "learn_skills": read_skills("learn", learn_skills),
        }},
    )
    return redirect(url_for("profile.my_profile"))