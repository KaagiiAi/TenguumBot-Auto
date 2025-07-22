import firebase_admin
from firebase_admin import db

async def memory_command(update, context):
    await update.message.reply_text("🧠 Ой санамжийг дуудаж байна...")

async def save_message_to_firebase(bot_id, user_id, user_text):
    ref = db.reference(f"bots/{bot_id}/users/{user_id}/messages")
    ref.push({"text": user_text})