import os
import logging
import base64
import json
import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from auto_push import auto_git_push

# 🔐 Firebase Key decode
firebase_key_str = os.getenv("FIREBASE_KEY_BASE64")
if not firebase_key_str:
    raise ValueError("❌ FIREBASE_KEY_BASE64 тохиргоо олдсонгүй!")

firebase_json = base64.b64decode(firebase_key_str).decode("utf-8")
firebase_dict = json.loads(firebase_json)

# 🔌 Firebase холболт
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://tenguunbotmemory-default-rtdb.firebaseio.com/'
    })

# 🧠 ChatGPT-ийн хариу генерацийн функц
def generate_chatgpt_response(user_text: str) -> str:
    if "сайн уу" in user_text.lower():
        return "Сайн уу! 😊 Юу туслах вэ?"
    return f"Та хэлсэн: {user_text}"

# 💬 Ердийн мессеж хадгалах болон хариу өгөх
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_text = update.message.text

    ref = db.reference(f"bots/tenguun/users/{user_id}/messages")
    ref.push({"text": user_text, "from": "user"})

    response = generate_chatgpt_response(user_text)
    await update.message.reply_text(response)

    ref.push({"text": response, "from": "bot"})

# 📌 Командууд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 TenguunBot ажиллаж байна!")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Систем хэвийн байна.")

async def whoami_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info = f"🧾 Таны мэдээлэл:\n\n👤 Нэр: {user.full_name}\n🆔 ID: {user.id}\n🔤 Username: @{user.username or 'байхгүй'}"
    await update.message.reply_text(info)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = db.reference(f"bots/tenguun/users/{user_id}")
    ref.delete()
    await update.message.reply_text("🗑 Бүх мэдээлэл устгагдлаа.")

async def push_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = auto_git_push()
    await update.message.reply_text(result)

# ▶️ Bot эхлүүлэх
app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("status", status_command))
app.add_handler(CommandHandler("whoami", whoami_command))
app.add_handler(CommandHandler("reset", reset_command))
app.add_handler(CommandHandler("push", push_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run_polling()