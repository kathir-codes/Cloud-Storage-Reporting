
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.file.models import File, FileStatus


def create_file(
    db: Session,
    user_id: UUID,
    original_filename: str,
    bucket_name: str,
    object_key: str,
    content_type: str,
) -> File:
    """Create a pending file record in PostgreSQL."""

    file = File(
        user_id=user_id,
        original_filename=original_filename,
        bucket_name=bucket_name,
        object_key=object_key,
        content_type=content_type,
        file_size=0,
        status=FileStatus.PENDING,
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    return file
