from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db
import uuid

def classify_task(text):
    result = {
        "category": "content" if "бичлэг" in text else "general",
        "type": "action",
        "priority": "high" if "өнөөдөр" in text else "normal",
        "goal_ref": "yes" if "зорилго" in text or "төлөвлөгөө" in text else "no",
        "text": text
    }
    return result

async def classify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("📝 Даалгаврын текстээ оруулна уу.")
        return

    task = classify_task(text)
    task_id = str(uuid.uuid4())
    task["id"] = task_id
    task["done"] = False

    ref = db.reference(f"bots/tenguun/users/{user_id}/tasks/{task_id}")
    ref.set(task)

    await update.message.reply_text(f"✅ Ангилсан даалгавар:\n📌 {task['text']}\n🗂 Төрөл: {task['category']}, Эрэмбэ: {task['priority']}")