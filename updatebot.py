# updatebot.py
import os
import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def update_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        repo_url = "https://github.com/KaagiiAi/TenguunBot-Auto.git"
        subprocess.run(["git", "init"])
        subprocess.run(["git", "remote", "add", "origin", repo_url])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "🔥 Auto update from Telegram bot"])
        subprocess.run(["git", "push", "-u", "origin", "main"])
        await update.message.reply_text("✅ Код амжилттай GitHub руу push хийгдлээ!")
    except Exception as e:
        await update.message.reply_text(f"❌ Push алдаа гарлаа: {e}")