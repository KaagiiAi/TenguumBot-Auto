from firebase_admin import db
import datetime

def save_message(bot_id, user_id, message):
    ref = db.reference(f'bots/{bot_id}/users/{user_id}/messages')
    ref.push({
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    })

def get_user_messages(bot_id, user_id):
    ref = db.reference(f'bots/{bot_id}/users/{user_id}/messages')
    return ref.get() or {}

def save_user_message(user_id, message):
    print(f"[MEMORY] Dummy save: user_id={user_id}, message='{message}'")