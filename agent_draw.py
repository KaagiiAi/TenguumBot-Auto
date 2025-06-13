import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def draw_image(prompt: str) -> str:
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return f"🖼️ Зураг гарлаа:\n{image_url}"
    except Exception as e:
        return f"❌ Зураг зурахад алдаа гарлаа: {e}"