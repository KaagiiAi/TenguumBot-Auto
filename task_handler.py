from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db

async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = db.reference(f"bots/tenguun/users/{user_id}/tasks")
    tasks = ref.get()

    if not tasks:
        await update.message.reply_text("📭 Даалгавар олдсонгүй.")
        return

    result = "📋 Бүх даалгаврууд:\n"
    for task_id, task in tasks.items():
        status = "✅" if task.get("done") else "🔄"
        result += f"{status} {task['text']} (ID: {task_id[:6]})\n"

    await update.message.reply_text(result)