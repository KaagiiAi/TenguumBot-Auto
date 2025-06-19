import subprocess
subprocess.run(["python3", "auto_push.py"])
import os
import json
import base64
import logging
import requests
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, db

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ✅ Firebase KEY-г ачааллах
firebase_key_str = os.getenv("FIREBASE_KEY_BASE64")
key_json_str = base64.b64decode(firebase_key_str).decode("utf-8")
firebase_cert = json.loads(key_json_str)
cred = credentials.Certificate(firebase_cert)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://tenguunbotmemory-default-rtdb.firebaseio.com'
    })

# ✅ Firebase функцууд
def get_user_ref(user_id):
    return db.reference(f"bots/tenguun/users/{user_id}")

def save_message(user_id, message):
    ref = get_user_ref(user_id).child("messages")
    ref.push({
        "text": message,
        "timestamp": datetime.utcnow().isoformat()
    })

def save_profile(user_id, username):
    ref = get_user_ref(user_id).child("profile")
    ref.set({
        "telegram_id": user_id,
        "name": username,
        "created_at": datetime.utcnow().isoformat()
    })

def update_goal(user_id, goal):
    ref = get_user_ref(user_id).child("profile/goal")
    ref.set(goal)

def update_status(user_id, status):
    ref = get_user_ref(user_id).child("profile/status")
    ref.set(status)

def delete_profile(user_id):
    get_user_ref(user_id).delete()

# ✅ Craiyon зураг үүсгэх
def generate_image(prompt):
    response = requests.post("https://backend.craiyon.com/generate", json={"prompt": prompt})
    if response.status_code == 200:
        data = response.json()
        return data.get("images", [])
    return []

# ✅ ChatGPT хариу үүсгэх
def generate_chatgpt_response(user_input):
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are Tenguun, a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "⚠️ Хариу үүсгэж чадсангүй."

# ✅ Коммандууд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_profile(user.id, user.username or user.full_name)
    await update.message.reply_text("👋 Сайн байна уу! Таны мэдээллийг хадгаллаа.")

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    goal_text = " ".join(context.args)
    update_goal(user.id, goal_text)
    await update.message.reply_text(f"🎯 Таны зорилго: {goal_text}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    status_text = " ".join(context.args)
    update_status(user.id, status_text)
    await update.message.reply_text(f"📌 Одоогийн байдал: {status_text}")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref = get_user_ref(user.id).child("profile")
    data = ref.get()
    if data:
        text = f"🧾 Таны мэдээлэл:\nНэр: {data.get('name')}\nЗорилго: {data.get('goal')}\nБайдал: {data.get('status')}"
    else:
        text = "Мэдээлэл олдсонгүй."
    await update.message.reply_text(text)

async def imagegen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    images = generate_image(prompt)
    if images:
        url = f"https://img.craiyon.com/{images[0]}"
        await update.message.reply_photo(photo=url)
    else:
        await update.message.reply_text("❌ Зураг үүсгэж чадсангүй.")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    delete_profile(user.id)
    await update.message.reply_text("♻️ Бүх мэдээллийг устгалаа!")

async def version_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 TenguunBot v4.0 | Firebase + OpenAI + Craiyon")

# ✅ Мессеж хүлээн авах
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_message(user.id, update.message.text)
    response = generate_chatgpt_response(update.message.text)
    await update.message.reply_text(response)

# ✅ Bot эхлүүлэх
logging.basicConfig(level=logging.INFO)
app = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("goal", goal))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("whoami", whoami))
app.add_handler(CommandHandler("image", imagegen))
app.add_handler(CommandHandler("reset", reset_command))
app.add_handler(CommandHandler("version", version_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()