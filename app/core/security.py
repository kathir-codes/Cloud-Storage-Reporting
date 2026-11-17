
import jwt
from jwt import PyJWKClient

from app.core.config import settings


COGNITO_ISSUER = (
    f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/"
    f"{settings.COGNITO_USER_POOL_ID}"
)

JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

jwks_client = PyJWKClient(JWKS_URL)


def verify_cognito_token(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=COGNITO_ISSUER,
        options={
            "verify_exp": True,
            "verify_iss": True,
            "verify_aud": False,
        },
    )

    if payload.get("token_use") != "access":
        raise ValueError("Invalid Cognito token type")

    if payload.get("client_id") != settings.COGNITO_APP_CLIENT_ID:
        raise ValueError("Invalid Cognito app client")

    return payload
