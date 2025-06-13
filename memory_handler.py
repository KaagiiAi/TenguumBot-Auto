from firebase_admin import db
from datetime import datetime

async def save_user_message(bot_id, user, message):
    user_ref = db.reference(f"bots/{bot_id}/users/{user.id}/messages")
    user_ref.push({
        "text": message,
        "timestamp": datetime.utcnow().isoformat()
    })