from services.firebase_service import db


# ===== CREATE USER =====
def create_user(user_dict):
    try:
        db.collection("users").document(user_dict["id"]).set(user_dict)
        return user_dict
    except Exception as e:
        print("Create User Error:", str(e))
        return None


# ===== GET USER BY EMAIL =====
def get_user_by_email(email):
    try:
        email = email.lower()

        users_ref = db.collection("users").where("email", "==", email).stream()

        for user in users_ref:
            data = user.to_dict()
            data["id"] = user.id  # 🔥 include document ID
            return data

        return None

    except Exception as e:
        print("Get User Error:", str(e))
        return None


# ===== GET USER BY ID =====
def get_user_by_id(user_id):
    try:
        doc = db.collection("users").document(user_id).get()

        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data

        return None

    except Exception as e:
        print("Get User By ID Error:", str(e))
        return None