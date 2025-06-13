def classify_task(message: str) -> str:
    message = message.lower()
    if "код" in message or "python" in message:
        return "Программчлалын даалгавар"
    elif "зураг" in message or "зураг үүсгэ" in message:
        return "Зураг үүсгэх"
    elif "өгүүлбэр" in message or "контент" in message:
        return "Контент үүсгэх"
    else:
        return "Ерөнхий AI даалгавар"