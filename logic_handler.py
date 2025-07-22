from telegram import Update
from telegram.ext import ContextTypes

async def logic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 /logic команд ажиллалаа! Хэрэглэгчийн логик хандлагыг хөгжүүлэх горим.")