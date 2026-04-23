import firebase_admin
from firebase_admin import storage
import uuid
import os

# initialize bucket (after firebase init)
bucket = storage.bucket()


def upload_image(file):
    try:
        if not file:
            return None

        # 🔥 Validate file type
        if not file.content_type.startswith("image/"):
            raise Exception("Only image files are allowed")

        # 🔥 Safe filename
        ext = os.path.splitext(file.filename)[1]
        filename = f"items/{uuid.uuid4()}{ext}"

        blob = bucket.blob(filename)

        # 🔥 Upload
        blob.upload_from_file(file, content_type=file.content_type)

        # 🔥 Make public (for now)
        blob.make_public()

        return blob.public_url

    except Exception as e:
        print("Upload Error:", str(e))
        return None