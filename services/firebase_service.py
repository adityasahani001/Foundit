import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import json
from dotenv import load_dotenv

# 🔥 LOAD ENV VARIABLES
load_dotenv()

# ===== INITIALIZE FIREBASE (ONLY ONCE) =====
if not firebase_admin._apps:

    firebase_config = os.getenv("FIREBASE_CONFIG")
    bucket_name = os.getenv("FIREBASE_BUCKET")

    # ❌ Safety checks
    if not firebase_config:
        raise Exception("FIREBASE_CONFIG not found in environment")

    if not bucket_name:
        raise Exception("FIREBASE_BUCKET not found in environment")

    # ✅ Convert JSON string → dict
    try:
        cred_dict = json.loads(firebase_config)
    except Exception as e:
        raise Exception(f"Invalid FIREBASE_CONFIG JSON: {e}")

    # ✅ Initialize Firebase
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
    item_id = item_dict.get("id")

    if not item_id:
        raise Exception("Item ID missing")

    db.collection("items").document(item_id).set(item_dict)
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
    try:
        if not item_id:
            raise Exception("Invalid item_id")

        db.collection("items").document(item_id).set(updated_data, merge=True)
        return True

    except Exception as e:
        print("🔥 FIRESTORE UPDATE ERROR:", e)
        return False


# ===== DELETE ITEM =====
def delete_item_from_db(item_id):
    db.collection("items").document(item_id).delete()
    return True