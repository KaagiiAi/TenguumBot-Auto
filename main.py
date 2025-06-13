import os
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from imagegen_craiyon import generate_image
from memory_handler import save_user_message
from profile_handler import init_user_profile
from openai_handler import generate_chatgpt_response

# Лог тохиргоо
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Firebase холболт
firebase_key_str = os.getenv("FIREBASE_KEY_BASE64")
key_json_str = base64.b64decode(firebase_key_str).decode("utf-8")
firebase_cert = json.loads(key_json_str)
cred = credentials.Certificate(firebase_cert)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://tenguunbotmemory-default-rtdb.firebaseio.com'
    })

bot_id = "TenguunBot"

# Командууд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await init_user_profile(bot_id, user)
    await update.message.reply_text("👋 Сайн байна уу! Би Тэнгүүн бот. Та асуулт асуугаарай!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот ажиллаж байна!")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🙋‍♂️ Таны нэр: {user.full_name}, ID: {user.id}")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = db.reference(f"bots/{bot_id}/users/{user_id}")
    ref.delete()
    await update.message.reply_text("🗑️ Таны мэдээлэл устгагдлаа.")

async def imagegen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("📸 Зураг үүсгэх үг оруулна уу. Жишээ: /imagegen future city")
        return
    image_url = generate_image(prompt)
    await update.message.reply_photo(photo=image_url)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await save_user_message(bot_id, user, text)
    response = generate_chatgpt_response(text)
    await update.message.reply_text(response)

# Bot run
app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("whoami", whoami))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("imagegen", imagegen))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()