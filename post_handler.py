from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db
import datetime
import uuid

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    post_text = " ".join(context.args)

    if not post_text:
        await update.message.reply_text("📝 Нийтлэх текстээ оруулна уу. Жишээ: /post AI Найзын видео №1")
        return

    post_id = str(uuid.uuid4())
    post_data = {
        "id": post_id,
        "text": post_text,
        "timestamp": str(datetime.datetime.utcnow()),
    }

    ref = db.reference(f"bots/tenguun/users/{user_id}/posts/{post_id}")
    ref.set(post_data)

    await update.message.reply_text(f"📢 Нийтлэл бүртгэгдлээ:\n🗣 {post_text}")