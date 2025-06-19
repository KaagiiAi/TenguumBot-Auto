import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import subprocess

# ✅ Лог тохиргоо
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ✅ Bot Token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Коммандууд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Сайн байна уу! TenguunBot Universal ажиллаж байна!")

async def push(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Код GitHub руу push хийгдэж байна...")
    result = subprocess.run(["python3", "push_code.py"], capture_output=True, text=True)
    await update.message.reply_text(f"✅ Push үр дүн:\n{result.stdout or result.stderr}")

async def updatebot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("♻️ Bot шинэчлэгдэж байна...")
    result = subprocess.run(["python3", "updatebot.py"], capture_output=True, text=True)
    await update.message.reply_text(f"✅ Update үр дүн:\n{result.stdout or result.stderr}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Auto Sync идэвхтэй байна!\n🟢 push_code.py болон updatebot.py бүрэн ажиллагаатай.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Танд туслах комманд олдсонгүй.")

# ✅ Апп эхлүүлэх
app = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ Комманд бүртгэх
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("push", push))
app.add_handler(CommandHandler("updatebot", updatebot))
app.add_handler(CommandHandler("status", status))
app.add_handler(MessageHandler(filters.COMMAND, unknown))

# ✅ Polling эхлүүлэх
print("🤖 Auto Sync Bot ажиллаж эхэллээ...")
app.run_polling()