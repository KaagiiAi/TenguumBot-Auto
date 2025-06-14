import requests
import uuid
import os

def generate_image_and_get_path(prompt: str) -> str:
    # Craiyon API ашиглаж зураг генерац хийх
    url = "https://backend.craiyon.com/generate"
    response = requests.post(url, json={"prompt": prompt})

    if response.status_code != 200:
        raise Exception("Зураг үүсгэхэд алдаа гарлаа!")

    image_data = response.json()["images"][0]  # эхний зургийг авна

    # Юник зураг нэр
    filename = f"craiyon_image_{uuid.uuid4().hex}.png"
    filepath = os.path.join("images", filename)

    # Фолдер үүсгээгүй бол үүсгэнэ
    os.makedirs("images", exist_ok=True)

    # Зураг хадгалах
    with open(filepath, "wb") as f:
        f.write(requests.get(f"https://img.craiyon.com/{image_data}").content)

    return filepath