from datetime import datetime
import uuid
import bcrypt


class User:
    def __init__(self, fullname, email, phone, password=None):
        self.id = str(uuid.uuid4())

        self.fullname = fullname
        self.email = email.strip().lower()   # ✅ improved
        self.phone = phone

        # 🔥 hash password if provided
        if password:
            self.password = self.hash_password(password)
        else:
            self.password = None

        self.role = "user"
        self.created_at = datetime.utcnow().isoformat()
        self.is_verified = False


    # ===== PASSWORD HASHING =====
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


    # ===== PASSWORD CHECK =====
    def check_password(self, password):
        if not self.password:
            return False   # ✅ prevent crash

        return bcrypt.checkpw(password.encode(), self.password.encode())


    # ===== convert object → dict (FOR DB ONLY) =====
    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at,
            "is_verified": self.is_verified
        }


    # ===== SAFE DATA (FOR API RESPONSE) =====
    def safe_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at,
            "is_verified": self.is_verified
        }


    # ===== dict → object =====
    @staticmethod
    def from_dict(data):
        user = User(
            fullname=data.get("fullname"),
            email=data.get("email"),
            phone=data.get("phone"),
            password=None  # 🔥 don't re-hash
        )

        user.id = data.get("id", user.id)
        user.password = data.get("password")  # already hashed
        user.role = data.get("role", "user")
        user.created_at = data.get("created_at", datetime.utcnow().isoformat())
        user.is_verified = data.get("is_verified", False)

        return user