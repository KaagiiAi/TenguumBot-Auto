import os
import requests
import uuid
import json
from datetime import datetime
from firebase_admin import db
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.content

def generate_caption(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def save_post_to_firebase(caption, image_data, user_id="system"):
    post_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    image_url = f"https://example.com/fakepath/{post_id}.png"

    post_data = {
        "id": post_id,
        "user_id": user_id,
        "caption": caption,
        "image_url": image_url,
        "created_at": timestamp,
        "posted": False
    }

    ref = db.reference(f"/tiktok/posts/{post_id}")
    ref.set(post_data)

    return post_data

def create_tiktok_post(prompt_text):
    caption = generate_caption(prompt_text)
    image_data = generate_image(prompt_text)
    post = save_post_to_firebase(caption, image_data)
    return post