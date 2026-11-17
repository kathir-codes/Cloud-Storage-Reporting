
import base64
import hashlib
import hmac

from app.core.config import settings


def generate_secret_hash(username: str) -> str:
    message = username + settings.COGNITO_APP_CLIENT_ID

    digest = hmac.new(
        settings.COGNITO_APP_CLIENT_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return base64.b64encode(digest).decode("utf-8")
