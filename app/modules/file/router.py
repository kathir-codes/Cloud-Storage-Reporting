
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.modules.file.schemas import (
    PresignedUploadRequest,
    PresignedUploadResponse,
)
from app.modules.file.service import create_file_upload_url
from app.modules.user.models import User

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/presigned-upload",
    response_model=PresignedUploadResponse,
)
def create_presigned_upload_url(
    payload: PresignedUploadRequest,
    current_user: User = Depends(get_current_user),
):
    return create_file_upload_url(
        filename=payload.filename,
        content_type=payload.content_type,
        user_id=current_user.id,
    )
