from datetime import datetime
import uuid


class Item:
    def __init__(
        self,
        title,
        category,
        description,
        date,
        location,
        item_type="found",
        image_url=None,
        user_id=None
    ):
        self.id = str(uuid.uuid4())

        self.title = title
        self.category = category
        self.description = description or ""
        self.date = date
        self.location = location

        # 🔥 safe type default
        self.type = item_type if item_type else "found"

        self.image_url = image_url
        self.user_id = user_id

        self.status = "active"
        self.created_at = datetime.utcnow().isoformat()

    # 🔥 convert object → dict
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "type": self.type,
            "image_url": self.image_url,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at
        }

    # 🔥 create object from dict
    @staticmethod
    def from_dict(data):
        item = Item(
            title=data.get("title"),
            category=data.get("category"),
            description=data.get("description"),
            date=data.get("date"),
            location=data.get("location"),
            item_type=data.get("type", "found"),  # ✅ safe default
            image_url=data.get("image_url"),
            user_id=data.get("user_id")
        )

        # 🔥 preserve original ID
        if data.get("id"):
            item.id = data["id"]

        item.status = data.get("status", "active")
        item.created_at = data.get(
            "created_at",
            datetime.utcnow().isoformat()
        )

        return item