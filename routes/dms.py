from flask import Blueprint, render_template, request
from flask_login import current_user
from flask_socketio import emit, join_room
from socket_event import socketio 

dms_bp = Blueprint("dms", __name__)

online_users = {}


@dms_bp.route("/dms")
def dms_page():
    if not current_user.is_authenticated:
        return "Unauthroized", 401

    return render_template("dms.html")

@socketio.on("connect", namespace="/dms")
def handle_connect():
    if not current_user.is_authenticated:
        return False

    user_id = str(current_user.get_id())

    online_users.setdefault(user_id, set()).add(request.sid)
    join_room(f"user:{user_id}", namespace="/dms")

@socketio.on("disconnect", namespace="/dms")
def handle_disconnect():
    for user_id, socket_ids in list(online_users.items()):
        socket_ids.discard(request.sid)

        if not socket_ids:
            del online_users[user_id]

@socketio.on("send_dm", namespace="/dms")
def handle_send_dm(data):
    if not current_user.is_authenticated:
        return

    if not isinstance(data, dict):
        return

    recipient_id = data.get("to")
    message = data.get("message")

    message = message.strip()
    sender_id = str(current_user.get_id())

    if recipient_id == sender_id:
        return

    emit(
        "receive_dm",
        {
            "from": sender_id,
            "message": message
        },
        to=f"user:{recipient_id}",
        namespace="/dms"
    )

    emit(
        "dm_sent",
        {
            "to": recipient_id,
            "message": message
        },
        to=request.sid,
        namespace="/dms"
    )