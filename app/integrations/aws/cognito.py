
import boto3

from app.core.config import settings


cognito = boto3.client(
    "cognito-idp",
    region_name=settings.AWS_REGION,
)