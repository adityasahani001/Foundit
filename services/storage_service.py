import uuid
import os
from firebase_admin import storage

# bucket already initialized via firebase_service
bucket = storage.bucket()


def upload_image(file):
    try:
        if not file:
            return None

        # ✅ Validate image
        if not file.content_type.startswith("image/"):
            raise Exception("Only image files allowed")

        # ✅ Generate filename
        ext = os.path.splitext(file.filename)[1]
        filename = f"items/{uuid.uuid4()}{ext}"

        blob = bucket.blob(filename)

        # ✅ Upload file
        blob.upload_from_file(file, content_type=file.content_type)

        # ✅ Make public
        blob.make_public()

        return blob.public_url

    except Exception as e:
        print("🔥 IMAGE UPLOAD ERROR:", e)
        return None