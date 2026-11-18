
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath

from sqlalchemy.orm import Session

from app.integrations.aws.s3 import (
    S3_BUCKET_NAME,
    generate_presigned_upload_url,
)
from app.modules.file import repository


def get_file_category(extension: str) -> str:
    categories = {
        "images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx"},
        "videos": {".mp4", ".mov", ".avi", ".mkv"},
        "audio": {".mp3", ".wav", ".aac"},
        "archives": {".zip", ".rar", ".7z"},
    }

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "others"


def create_file_upload_url(
    db: Session,
    filename: str,
    content_type: str,
    user_id: uuid.UUID,
):
    extension = PurePosixPath(filename).suffix.lower()

    category = get_file_category(extension)

    upload_date = datetime.now(timezone.utc).date().isoformat()

    object_key = (
        f"users/{user_id}/{category}/"
        f"{upload_date}/{uuid.uuid4()}{extension}"
    )

    # Generate the S3 upload URL.
    upload_url = generate_presigned_upload_url(
        object_key=object_key,
        content_type=content_type,
    )

    # Save file metadata in PostgreSQL.
    repository.create_file(
        db=db,
        user_id=user_id,
        original_filename=filename,
        bucket_name=S3_BUCKET_NAME,
        object_key=object_key,
        content_type=content_type,
    )

    return {
        "upload_url": upload_url,
        "object_key": object_key,
        "expires_in": 300,
    }

# upload_url = generate_presigned_upload_url(
#     object_key="users/61f3dd7a-0031-7071-9709-78a9dd614e7e/documents/2026-11-18/1e41280a-1a21-4fc3-8b87-a234002fb094.txt",
#     content_type="text/plain",
# )

# print(upload_url)