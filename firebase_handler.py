import firebase_admin
from firebase_admin import credentials, db
import os
import base64
import json

def initialize_firebase():
    key_base64 = os.getenv("FIREBASE_KEY_BASE64")
    if not key_base64:
        raise ValueError("❌ FIREBASE_KEY_BASE64 not found")

    key_json = json.loads(base64.b64decode(key_base64).decode("utf-8"))
    cred = credentials.Certificate(key_json)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "databaseURL": os.getenv("FIREBASE_DB_URL")
        })