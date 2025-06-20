from firebase_admin import db
from telegram import Update
from telegram.ext import ContextTypes

async def classify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("❗ Жишээ:\n/classify Гүйх, дасгал хийх, ус уух")
        return

    # Firebase рүү хадгалах
    ref = db.reference(f'bots/tenguun/users/{user_id}/tasks')
    ref.push({
        "task": text,
        "status": "pending"
    })

    await update.message.reply_text(f"✅ Даалгавар хадгалагдлаа:\n{text}")