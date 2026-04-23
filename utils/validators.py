import re


# ===== ITEM VALIDATION =====
def validate_item_data(data):
    required_fields = ["title", "category", "date", "location"]

    for field in required_fields:
        value = data.get(field)
        if not value or str(value).strip() == "":
            return False, f"{field.capitalize()} is required"

    return True, None


# ===== EMAIL VALIDATION =====
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# ===== PHONE VALIDATION =====
def is_valid_phone(phone):
    # simple 10-digit check (India friendly)
    return phone.isdigit() and len(phone) == 10


# ===== USER VALIDATION =====
def validate_user_data(data):
    required_fields = ["fullname", "email", "phone", "password"]

    for field in required_fields:
        value = data.get(field)
        if not value or str(value).strip() == "":
            return False, f"{field.capitalize()} is required"

    email = data.get("email").strip().lower()
    phone = data.get("phone").strip()
    password = data.get("password")

    # 🔥 email check
    if not is_valid_email(email):
        return False, "Invalid email format"

    # 🔥 phone check
    if not is_valid_phone(phone):
        return False, "Phone must be 10 digits"

    # 🔥 password check
    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    return True, None