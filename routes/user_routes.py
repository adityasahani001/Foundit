from flask import Blueprint, session, jsonify
from services.user_service import get_user_by_id

user_bp = Blueprint('user', __name__)


# ===== GET CURRENT LOGGED-IN USER =====
@user_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({
                "success": False,
                "message": "User not logged in"
            }), 401

        user = get_user_by_id(user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "fullname": user.get("fullname"),   # ✅ standard key
                "email": user.get("email"),
                "phone": user.get("phone")
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== GET USER BY ID (FOR ITEM VIEW / CONTACT) =====
@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "fullname": user.get("fullname"),
                "email": user.get("email"),
                "phone": user.get("phone")
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500