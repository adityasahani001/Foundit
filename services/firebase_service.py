import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import json

# Initialize Firebase ONLY ONCE
if not firebase_admin._apps:

    firebase_key = os.environ.get("FIREBASE_KEY")
    bucket_name = os.environ.get("FIREBASE_BUCKET")

    if not firebase_key:
        raise Exception("FIREBASE_KEY not found in environment")

    # 🔥 Convert JSON string → dict
    cred_dict = json.loads(firebase_key)

    cred = credentials.Certificate(cred_dict)

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