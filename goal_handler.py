from telegram import Update
from telegram.ext import ContextTypes

async def goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.strip() == "/goal":
        await update.message.reply_text("🎯 Та зорилгоо бичнэ үү. Жишээ: /goal TikTok бичлэгээр 1000 дагагч авах.")
    else:
        await update.message.reply_text(f"🎯 Зорилго бүртгэгдлээ!\n{text[6:].strip()}")