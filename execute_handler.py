from firebase_admin import db
from telegram import Update
from telegram.ext import ContextTypes

async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = db.reference(f'bots/tenguun/users/{user_id}/tasks')
    tasks = ref.get()

    if not tasks:
        await update.message.reply_text("📭 Гүйцэтгэх даалгавар олдсонгүй.")
        return

    done = 0
    for key, value in tasks.items():
        if value.get("status") == "pending":
            ref.child(key).update({"status": "done"})
            done += 1

    await update.message.reply_text(f"✅ Гүйцэтгэсэн даалгавар: {done} ширхэг.")