from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db

async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("❗ Даалгаврын ID-г оруулна уу: /execute [id]")
        return

    task_id = context.args[0]
    ref = db.reference(f"bots/tenguun/users/{user_id}/tasks/{task_id}")
    task = ref.get()

    if not task:
        await update.message.reply_text("⚠️ Ийм ID-тай даалгавар олдсонгүй.")
        return

    if task.get("done"):
        await update.message.reply_text("✅ Энэ даалгавар аль хэдийн гүйцэтгэсэн байна.")
        return

    task["done"] = True
    ref.update(task)

    await update.message.reply_text(f"🤖 Даалгавар гүйцэтгэсэн: {task['text']}")