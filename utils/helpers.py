import uuid
from datetime import datetime


# 🔥 Generate unique ID
def generate_id():
    return str(uuid.uuid4())


# 🔥 Current timestamp
def current_time():
    return datetime.now().isoformat()


# 🔥 Format item before saving
def format_item(data, user_id):
    return {
        "id": generate_id(),
        "title": data.get("title"),
        "category": data.get("category"),
        "description": data.get("description"),
        "date": data.get("date"),
        "location": data.get("location"),
        "type": data.get("type"),
        "user_id": user_id,
        "created_at": current_time()
    }