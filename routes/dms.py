from flask import Blueprint, render_template, request
from flask_login import current_user
from flask_socketio import emit, join_room
from bson import ObjectId
from .profile import find_user
from socket_event import socketio 
from db import db

dms_bp = Blueprint("dms", __name__)

online_users = {}


@dms_bp.route("/dms/<user_id>", methods=["GET", "POST"])
def dms_page(user_id):
    if not current_user.is_authenticated:
        return "Unauthroized", 401

    sender_id = str(current_user.get_id())
    receiver_id = str(user_id)
    sender = find_user(sender_id)
    receiver = find_user(receiver_id)
    conversation = retrieve_conversation(sender_id, receiver_id)

    return render_template("dms.html", sender=sender, receiver=receiver, messages=conversation["messages"])

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

    recipient_id = str(data.get("to"))
    message = data.get("message")

    message = message.strip()
    sender_id = str(current_user.get_id())

    sender_user = find_user(sender_id)
    recipient_user = find_user(recipient_id)

    if recipient_id == sender_id:
        return

    conversation = retrieve_conversation(sender_id, recipient_id)
    save_conversation(conversation["_id"], sender_id, message)

    emit(
        "receive_dm",
        {
            "from_id": sender_id,
            "from_username": sender_user.get("username"),
            "message": message
        },
        to=f"user:{recipient_id}",
        namespace="/dms"
    )

    emit(
        "dm_sent",
        {
            "to_id": recipient_id,
            "to_username": recipient_user.get("username"),
            "message": message
        },
        to=request.sid,
        namespace="/dms"
    )

def retrieve_conversation(user1_id, user2_id):
    participants = sorted([ObjectId(user1_id), ObjectId(user2_id)], key=str)

    conversation = db.conversations.find_one({"participants" : participants})

    if conversation is None:
        conversation = {
            "participants" : participants,
            "messages": []
        }

        result = db.conversations.insert_one(conversation)
        conversation["_id"] = result.inserted_id
    return conversation

def save_conversation(conversation_id, sender_id, message):
    result = db.conversations.update_one(
        {"_id" : conversation_id},
        {
            "$push": {
                "messages": {
                    "sender_id": ObjectId(sender_id),
                    "message": message
                }
            }
        }
    )

    return result.modified_count == 1 #checks the update is valid