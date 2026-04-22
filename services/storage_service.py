import firebase_admin
from firebase_admin import storage
import uuid

# initialize bucket (after firebase init)
bucket = storage.bucket()


def upload_image(file):
    if not file:
        return None

    filename = f"items/{uuid.uuid4()}_{file.filename}"
    blob = bucket.blob(filename)

    blob.upload_from_file(file, content_type=file.content_type)

    # make public (for now)
    blob.make_public()

    return blob.public_url