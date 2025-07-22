import firebase_admin
from firebase_admin import credentials, db
import time
import subprocess
import os

# Firebase-ийн тохиргоо
firebase_key_base64 = os.getenv("FIREBASE_KEY_BASE64")
if not firebase_key_base64:
    raise ValueError("FIREBASE_KEY_BASE64 орчин тохируулаагүй байна!")

import base64
key_json_str = base64.b64decode(firebase_key_base64).decode("utf-8")
cred = credentials.Certificate(eval(key_json_str))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tenguunbotmemory-default-rtdb.firebaseio.com/'
})

# Bot ID
BOT_ID = "TenguunUniversal"

# Trigger сонсох зам
TRIGGER_PATH = f"bots/{BOT_ID}/system/trigger_now"

def run_main_py():
    print("🔥 main.py-г ажиллуулж байна...")
    subprocess.Popen(["python3", "main.py"])

def listen_trigger():
    ref = db.reference(TRIGGER_PATH)
    print(f"👂 Trigger-г сонсож байна: {TRIGGER_PATH}")
    while True:
        value = ref.get()
        if value == True:
            print("🚀 Trigger илэрлээ!")
            run_main_py()
            ref.set(False)  # Trigger-г reset хийж байна
        time.sleep(2)

if __name__ == "__main__":
    listen_trigger()