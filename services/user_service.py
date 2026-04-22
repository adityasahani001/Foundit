from services.firebase_service import db


# ===== CREATE USER =====
def create_user(user_dict):
    db.collection("users").document(user_dict["id"]).set(user_dict)
    return user_dict


# ===== GET USER BY EMAIL =====
def get_user_by_email(email):
    users_ref = db.collection("users").where("email", "==", email).stream()

    for user in users_ref:
        return user.to_dict()

    return None