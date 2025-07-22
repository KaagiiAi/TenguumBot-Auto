import os
import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def push_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🤖 Auto update from Telegram bot"], check=True)
        subprocess.run(["git", "push"], check=True)
        await update.message.reply_text("✅ Код GitHub руу амжилттай пуш хийгдлээ.")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Push амжилтгүй боллоо: {e}")