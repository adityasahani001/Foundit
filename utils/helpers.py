import uuid
from datetime import datetime


# ===== GENERATE UNIQUE ID =====
def generate_id():
    return str(uuid.uuid4())


# ===== CURRENT TIMESTAMP =====
def current_time():
    return datetime.utcnow().isoformat()


# ===== SAFE VALUE GETTER =====
def safe_get(data, key, default=""):
    value = data.get(key, default)
    return str(value).strip() if value else default


# ===== FORMAT ITEM BEFORE SAVING =====
def format_item(data, user_id):
    return {
        "id": generate_id(),

        "title": safe_get(data, "title"),
        "category": safe_get(data, "category"),
        "description": safe_get(data, "description"),

        "date": safe_get(data, "date"),
        "location": safe_get(data, "location"),

        "type": safe_get(data, "type", "found"),  # default

        "user_id": user_id,

        "status": "active",  # future use (matched, returned, etc.)

        "created_at": current_time()
    }