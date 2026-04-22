def validate_item_data(data):
    required_fields = ["title", "category", "date", "location"]

    for field in required_fields:
        if not data.get(field):
            return False, f"{field} is required"

    return True, None


def validate_user_data(data):
    required_fields = ["fullname", "email", "phone", "password"]

    for field in required_fields:
        if not data.get(field):
            return False, f"{field} is required"

    if len(data.get("password", "")) < 6:
        return False, "Password must be at least 6 characters"

    return True, None