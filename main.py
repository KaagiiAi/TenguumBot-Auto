import os
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from openai import OpenAI
from push_code import push_code_command

# Firebase config
firebase_key = os.getenv("FIREBASE_KEY_BASE64")
if not firebase_key:
    raise ValueError("❌ FIREBASE_KEY_BASE64 not found.")
firebase_json = json.loads(base64.b64decode(firebase_key).decode())
cred = credentials.Certificate(firebase_json)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DB_URL")
    })

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_chatgpt_response(user_text):
    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Чи туслах."},
            {"role": "user", "content": user_text}
        ]
    )
    return completion.choices[0].message.content

def save_message(user_id, text):
    ref = db.reference(f"bots/tenguun/users/{user_id}/messages")
    ref.push({"text": text, "role": "user"})

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    save_message(user_id, text)
    reply = generate_chatgpt_response(text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 TenguunBot ажиллаж байна!")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(f"🧾 Та: {u.first_name} (@{u.username}) | ID: {u.id}")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db.reference(f"bots/tenguun/users/{user_id}/messages").delete()
    await update.message.reply_text("♻️ Санах ой шинэчлэгдлээ!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Систем хэвийн байна.")

# Telegram bot
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("whoami", whoami))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("push", push_code_command))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()