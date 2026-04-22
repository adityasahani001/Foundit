import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get values from .env
cred_path = os.getenv("FIREBASE_KEY_PATH")
bucket_name = os.getenv("FIREBASE_BUCKET")

# Initialize Firebase ONLY ONCE
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': bucket_name
    })

# Firestore DB
db = firestore.client()

# Storage bucket
bucket = storage.bucket()


# ===== ADD ITEM =====
def add_item_to_db(item_dict):
    doc_ref = db.collection("items").document(item_dict["id"])
    doc_ref.set(item_dict)
    return item_dict


# ===== GET ALL ITEMS =====
def get_all_items():
    docs = db.collection("items").stream()
    items = []

    for doc in docs:
        items.append(doc.to_dict())

    return items


# ===== DELETE ITEM =====
def delete_item_from_db(item_id):
    db.collection("items").document(item_id).delete()
    return True