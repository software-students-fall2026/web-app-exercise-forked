from bson.errors import InvalidId
from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask import Blueprint, render_template, abort, redirect, request, url_for
from flask_login import current_user, login_required
from db import db

moderation_bp = Blueprint("moderation", __name__, url_prefix="/moderation")

@moderation_bp.route("/")
@login_required
def moderation():
    if current_user.role != "moderator":
        abort(403)
        
    all_reports = list(db.reports.find())
    
    return render_template("moderation.html", reports=all_reports)