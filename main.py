import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai_handler import generate_chatgpt_response
from profile_handler import handle_profile
from memory_handler import save_user_message
from classify_handler import classify_command
from execute_handler import execute_command
from push_code import push_to_github

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Коммандууд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Сайн байна уу! TenguunBot Universal ажиллаж байна!")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Auto Sync идэвхтэй байна!")

async def push_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Код GitHub руу push хийгдэж байна...")
    result = push_to_github()
    await update.message.reply_text(f"✅ Push үр дүн:\n{result}")

async def updatebot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("♻️ Bot шинэчлэгдэж байна...")
    os.system("python3 main.py &")
    await update.message.reply_text("✅ Update үр дүн:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    save_user_message(user_id, user_text)
    response = generate_chatgpt_response(user_text)
    await update.message.reply_text(response)

# ✅ Bot эхлүүлэх
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("status", status_command))
app.add_handler(CommandHandler("push", push_command))
app.add_handler(CommandHandler("updatebot", updatebot_command))
app.add_handler(CommandHandler("classify", classify_command))
app.add_handler(CommandHandler("execute", execute_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()