from services.firebase_service import db
from datetime import datetime


def save_feedback(data):
    try:
        feedback_ref = db.collection("feedback")

        feedback = {
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
            "created_at": datetime.utcnow().isoformat()
        }

        feedback_ref.add(feedback)

        return True

    except Exception as e:
        print("🔥 Feedback Error:", e)
        return False