import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import json

# ===== INITIALIZE FIREBASE (ONLY ONCE) =====
if not firebase_admin._apps:

    firebase_config = os.getenv("FIREBASE_CONFIG")
    bucket_name = os.getenv("FIREBASE_BUCKET")

    # ❌ Safety check
    if not firebase_config:
        raise Exception("FIREBASE_CONFIG not found in environment")

    # ✅ Convert JSON string → dict
    try:
        cred_dict = json.loads(firebase_config)
    except Exception as e:
        raise Exception(f"Invalid FIREBASE_CONFIG JSON: {e}")

    # ✅ Initialize Firebase using JSON
    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred, {
        "storageBucket": bucket_name
    })

# ===== FIRESTORE DB =====
db = firestore.client()

# ===== STORAGE BUCKET =====
bucket = storage.bucket()


# ===== ADD ITEM =====
def add_item_to_db(item_dict):
    db.collection("items").document(item_dict["id"]).set(item_dict)
    return item_dict


# ===== GET ALL ITEMS =====
def get_all_items():
    docs = db.collection("items").stream()
    return [doc.to_dict() for doc in docs]


# ===== GET ITEMS BY USER =====
def get_items_by_user(user_id):
    docs = db.collection("items").where("user_id", "==", user_id).stream()
    return [doc.to_dict() for doc in docs]


# ===== GET SINGLE ITEM =====
def get_item_by_id(item_id):
    doc = db.collection("items").document(item_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


# ===== UPDATE ITEM =====
def update_item_in_db(item_id, updated_data):
    db.collection("items").document(item_id).update(updated_data)
    return True


# ===== DELETE ITEM =====
def delete_item_from_db(item_id):
    db.collection("items").document(item_id).delete()
    return True