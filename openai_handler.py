import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_chatgpt_response(text):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI алдаа: {e}"