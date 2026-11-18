
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import verify_cognito_token
from app.database.connection import SessionLocal
from app.integrations.aws.cognito import cognito
from app.modules.auth.decorators import handle_cognito_exceptions
from app.modules.auth.token_utils import generate_secret_hash
from app.modules.user.service import sync_cognito_user


def _sync_authenticated_user(access_token: str):
    """Verify Cognito user and synchronize with PostgreSQL."""

    # Verify the access token.
    token_payload = verify_cognito_token(access_token)

    # Retrieve user attributes from Cognito.
    response = cognito.get_user(AccessToken=access_token)

    attributes = {
        item["Name"]: item["Value"]
        for item in response.get("UserAttributes", [])
    }

    cognito_sub = token_payload["sub"]
    email = attributes.get("email")
    name = attributes.get("name")

    if not email:
        raise AuthenticationError(
            message="User email is missing from Cognito."
        )

    # Synchronize user with PostgreSQL.
    with SessionLocal() as db:
        return sync_cognito_user(
            db=db,
            cognito_sub=cognito_sub,
            email=email,
            name=name,
        )


@handle_cognito_exceptions
def login_user(email: str, password: str):
    """Authenticate user with Cognito."""

    response = cognito.initiate_auth(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
            "SECRET_HASH": generate_secret_hash(email),
        },
    )

    result = response.get("AuthenticationResult")

    if result:
        _sync_authenticated_user(result["AccessToken"])
        return result

    if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        return {
            "ChallengeName": response["ChallengeName"],
            "Session": response["Session"],
        }

    raise AuthenticationError(
        message="Authentication could not be completed."
    )


@handle_cognito_exceptions
def complete_new_password(
    email: str,
    session: str,
    new_password: str,
):
    """Complete Cognito new password challenge."""

    response = cognito.respond_to_auth_challenge(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        ChallengeName="NEW_PASSWORD_REQUIRED",
        Session=session,
        ChallengeResponses={
            "USERNAME": email,
            "NEW_PASSWORD": new_password,
            "SECRET_HASH": generate_secret_hash(email),
        },
    )

    result = response.get("AuthenticationResult")

    if not result:
        raise AuthenticationError(
            message="Password change could not be completed."
        )

    _sync_authenticated_user(result["AccessToken"])

    return result


@handle_cognito_exceptions
def refresh_access_token(email: str, refresh_token: str):
    """Refresh Cognito access token."""

    response = cognito.initiate_auth(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "USERNAME": email,
            "REFRESH_TOKEN": refresh_token,
            "SECRET_HASH": generate_secret_hash(email),
        },
    )

    result = response.get("AuthenticationResult")

    if not result:
        raise AuthenticationError(
            message="Token refresh could not be completed."
        )

    return result
