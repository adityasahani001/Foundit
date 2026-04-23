import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from dotenv import load_dotenv

# 🔥 Load environment variables
load_dotenv()

# ===== INITIALIZE FIREBASE (ONLY ONCE) =====
if not firebase_admin._apps:

    cred_path = os.getenv("FIREBASE_KEY_PATH")
    bucket_name = os.getenv("FIREBASE_BUCKET")

    # ❌ Safety check
    if not cred_path:
        raise Exception("FIREBASE_KEY_PATH not found in environment")

    if not os.path.exists(cred_path):
        raise Exception(f"Firebase key file not found at: {cred_path}")

    # ✅ Use file path (correct method)
    cred = credentials.Certificate(cred_path)

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

