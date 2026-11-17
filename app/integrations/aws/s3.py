
import boto3
from botocore.config import Config

from app.core.config import settings



s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    endpoint_url=f"https://s3.{settings.AWS_REGION}.amazonaws.com",
)


S3_BUCKET_NAME = settings.S3_BUCKET_NAME


def generate_presigned_upload_url(
    object_key: str,
    content_type: str,
    expiration: int = 300,
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=expiration,
    )
