from flask import Blueprint, request, jsonify, session
from models.item_model import Item
from services.firebase_service import add_item_to_db, get_all_items, delete_item_from_db
from services.storage_service import upload_image
from services.matching_service import match_items
from services.firebase_service import update_item_in_db
from services.user_service import get_user_by_id

item_bp = Blueprint('items', __name__)


# ===== ADD ITEM =====
@item_bp.route('/add', methods=['POST'])
def add_item():
    try:
        # 🔒 CHECK LOGIN
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Unauthorized. Please login first."
            }), 401

        user_id = session.get("user_id")

        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        item_type = request.form.get("type", "found")

        # 🔥 validation
        if not title or not category or not date or not location:
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # 🔥 create item model
        item = Item(
            title=title,
            category=category,
            description=description,
            date=date,
            location=location,
            item_type=item_type
        )

        # ✅ ATTACH USER
        item.user_id = user_id

        # 🔥 upload image (if exists)
        file = request.files.get("image")
        print("🔥 FILE RECEIVED:", file)
        image_url = None
        if file and file.filename != "":
            image_url = upload_image(file)
        item.image_url = image_url


        # 🔥 save to Firebase
        saved_item = add_item_to_db(item.to_dict())

        return jsonify({
            "success": True,
            "message": "Item added successfully",
            "item": saved_item
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== GET ALL ITEMS =====
@item_bp.route('/all', methods=['GET'])
def get_items():
    try:
        items = get_all_items()

        updated_items = []

        for item in items:
            user = get_user_by_id(item.get("user_id"))

            item["user_name"] = user.get("fullname") if user else "Unknown"

            updated_items.append(item)

        return jsonify({
            "success": True,
            "count": len(updated_items),
            "items": updated_items
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== GET USER ITEMS (NEW) =====
@item_bp.route('/my-items', methods=['GET'])
def get_my_items():
    try:
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Unauthorized"
            }), 401

        user_id = session.get("user_id")

        items = get_all_items()
        user_items = [item for item in items if item.get("user_id") == user_id]

        return jsonify({
            "success": True,
            "count": len(user_items),
            "items": user_items
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== MATCH ITEMS =====
@item_bp.route('/match', methods=['GET'])
def get_matches():
    try:
        items = get_all_items()

        matches = match_items(items)

        return jsonify({
            "success": True,
            "count": len(matches),
            "matches": matches
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ===== DELETE ITEM =====
@item_bp.route('/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Unauthorized"
            }), 401

        user_id = session.get("user_id")

        # 🔥 Get all items
        items = get_all_items()
        item = next((i for i in items if i.get("id") == item_id), None)

        if not item:
            return jsonify({
                "success": False,
                "message": "Item not found"
            }), 404

        # 🔒 OWNER CHECK
        if item.get("user_id") != user_id:
            return jsonify({
                "success": False,
                "message": "You can only delete your own items"
            }), 403

        delete_item_from_db(item_id)

        return jsonify({
            "success": True,
            "message": "Item deleted successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

# ===== UPDATE ITEM =====
@item_bp.route('/update/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Unauthorized"
            }), 401

        user_id = session.get("user_id")

        # 🔥 FETCH ITEM FIRST (IMPORTANT SECURITY)
        items = get_all_items()
        item = next((i for i in items if i.get("id") == item_id), None)

        if not item:
            return jsonify({
                "success": False,
                "message": "Item not found"
            }), 404

        # 🔒 OWNER CHECK
        if item.get("user_id") != user_id:
            return jsonify({
                "success": False,
                "message": "You can only update your own items"
            }), 403

        # 🔥 HANDLE BOTH JSON + FORM DATA
        if request.content_type and "multipart/form-data" in request.content_type:
            data = request.form.to_dict()
            file = request.files.get("image")
        else:
            data = request.get_json()
            file = None

        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400

        # 🔥 HANDLE IMAGE UPDATE
        if file and file.filename != "":
            image_url = upload_image(file)
            data["image_url"] = image_url

        success = update_item_in_db(item_id, data)

        if success:
            return jsonify({
                "success": True,
                "message": "Item updated successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Update failed"
            }), 500

    except Exception as e:
        print("🔥 UPDATE ROUTE ERROR:", e)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

# ===== CLAIM ITEM =====
@item_bp.route('/claim/<item_id>', methods=['POST'])
def claim_item(item_id):
    try:
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Login required"
            }), 401

        user_id = session.get("user_id")

        # 🔥 (Basic version - just response)
        # Later you can store this in DB

        return jsonify({
            "success": True,
            "message": f"Claim request sent for item {item_id}"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500