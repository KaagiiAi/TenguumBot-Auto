from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db

async def feed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = db.reference(f"bots/tenguun/users/{user_id}/posts")
    posts = ref.get()

    if not posts:
        await update.message.reply_text("📭 Хуваалцсан нийтлэл алга.")
        return

    text = "📰 Нийтлэлүүд:\n"
    for post_id, post in sorted(posts.items(), key=lambda x: x[1]['timestamp'], reverse=True):
        text += f"📌 {post['text']}\n"

    await update.message.reply_text(text)