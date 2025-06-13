import hashlib

def generate_image(prompt: str):
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return f"https://www.thiswaifudoesnotexist.net/example-{prompt_hash[-3:]}.jpg"