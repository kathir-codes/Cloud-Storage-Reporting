import uuid
from pathlib import PurePosixPath

from app.integrations.aws.s3 import generate_presigned_upload_url

def create_file_upload_url(
    filename: str,
    content_type: str,
    cognito_sub: str,
):
    extension = PurePosixPath(filename).suffix

    object_key = (
        f"users/{cognito_sub}/uploads/{uuid.uuid4()}{extension}"
    )

    upload_url = generate_presigned_upload_url(
        object_key=object_key,
        content_type=content_type,
    )

    return {
        "upload_url": upload_url,
        "object_key": object_key,
        "expires_in": 300,
    }