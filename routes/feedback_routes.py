from flask import Blueprint, request, jsonify
from services.feedback_service import save_feedback

feedback_bp = Blueprint('feedback', __name__)


@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        data = request.json

        if not data.get("name") or not data.get("email") or not data.get("message"):
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        success = save_feedback(data)

        if success:
            return jsonify({
                "success": True,
                "message": "Feedback submitted successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to save feedback"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500