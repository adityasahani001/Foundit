from flask import Blueprint, request, jsonify, session
from models.user_model import User
from services.user_service import (
    create_user,
    get_user_by_email
)

auth_bp = Blueprint('auth', __name__)


# ===== REGISTER =====
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        fullname = data.get("fullname")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        # 🔥 validation
        if not fullname or not email or not phone or not password:
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        # 🔥 check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({
                "success": False,
                "message": "User already exists"
            }), 409

        # 🔥 create user model (auto hashes password)
        user = User(fullname, email, phone, password)

        # 🔥 save to Firebase
        create_user(user.to_dict())

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== LOGIN =====
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password required"
            }), 400

        # 🔥 get user from DB
        user_data = get_user_by_email(email)

        if not user_data:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        # 🔥 convert dict → model
        user = User.from_dict(user_data)

        # 🔥 check password
        if not user.check_password(password):
            return jsonify({
                "success": False,
                "message": "Invalid password"
            }), 401

        # ✅ STORE SESSION
        session["user_id"] = user.id

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== LOGOUT =====
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop("user_id", None)

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


# ===== CHECK SESSION =====
@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    user_id = session.get("user_id")

    if user_id:
        return jsonify({
            "logged_in": True,
            "user_id": user_id
        })
    else:
        return jsonify({
            "logged_in": False
        })