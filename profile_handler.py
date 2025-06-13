from firebase_admin import db
from datetime import datetime

async def init_user_profile(bot_id, user):
    user_ref = db.reference(f"bots/{bot_id}/users/{user.id}/profile")
    if not user_ref.get():
        user_ref.set({
            "name": user.full_name,
            "telegram_id": user.id,
            "created_at": datetime.utcnow().isoformat()
        })