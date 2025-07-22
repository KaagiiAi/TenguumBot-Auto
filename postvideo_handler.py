from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from firebase_admin import db

async def postvideo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts_ref = db.reference("/tiktok/posts")
    all_posts = posts_ref.get()
    
    if not all_posts:
        await update.message.reply_text("❌ Пост олдсонгүй.")
        return
    
    latest_post = sorted(all_posts.values(), key=lambda x: x["created_at"], reverse=True)[0]

    caption = latest_post["caption"]
    image_url = latest_post["image_url"]
    post_id = latest_post["id"]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Пост хийх", url=image_url)]
    ])

    await update.message.reply_photo(
        photo=image_url,
        caption=f"📝 {caption}\n\n🆔 Пост ID: `{post_id}`",
        parse_mode="Markdown",
        reply_markup=keyboard
    )