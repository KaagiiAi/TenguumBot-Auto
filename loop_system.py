from telegram import Update
from telegram.ext import ContextTypes

async def selfeval_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔁 Tenguun өөрийгөө шалгаж, системээ шинэчилж байна...")