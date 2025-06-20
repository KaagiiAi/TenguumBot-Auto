import datetime
from firebase_admin import db

def store_profile(bot_id, user_id, name):
    ref = db.reference(f'bots/{bot_id}/users/{user_id}/profile')
    ref.set({
        'name': name,
        'telegram_id': user_id,
        'created_at': datetime.datetime.now().isoformat()
    })

def load_profile(bot_id, user_id):
    ref = db.reference(f'bots/{bot_id}/users/{user_id}/profile')
    return ref.get()
    # profile_handler.py
def handle_profile(user_id):
    print(f"Profile data not handled for {user_id} (function placeholder)")