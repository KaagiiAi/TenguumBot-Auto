from telegram import Update
from telegram.ext import ContextTypes
from firebase_admin import db
import uuid
import datetime

async def plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    plan_text = " ".join(context.args)

    if not plan_text:
        await update.message.reply_text("📋 Төлөвлөгөөгөө бичнэ үү. Жишээ: /plan TikTok бичлэг 7 хоногт 3 удаа")
        return

    plan_id = str(uuid.uuid4())
    plan_data = {
        "id": plan_id,
        "text": plan_text,
        "created_at": str(datetime.datetime.utcnow()),
    }

    ref = db.reference(f"bots/tenguun/users/{user_id}/plans/{plan_id}")
    ref.set(plan_data)

    await update.message.reply_text(f"✅ Төлөвлөгөө хадгалагдлаа:\n📌 {plan_text}")