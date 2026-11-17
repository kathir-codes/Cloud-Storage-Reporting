
from botocore.exceptions import ClientError

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.integrations.aws.cognito import cognito
from app.modules.auth.decorators import handle_cognito_exceptions
from app.modules.auth.token_utils import generate_secret_hash


@handle_cognito_exceptions
def login_user(email: str, password: str):
    username = email

    response = cognito.initiate_auth(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
            "SECRET_HASH": generate_secret_hash(username),
        },
    )

    result = response.get("AuthenticationResult")

    if result:
        return result

    if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        return {
            "ChallengeName": response["ChallengeName"],
            "Session": response["Session"],
        }

    raise AuthenticationError(
        message="Authentication could not be completed.",
    )



@handle_cognito_exceptions
def complete_new_password(
    email: str,
    session: str,
    new_password: str,
):
    username = email

    response = cognito.respond_to_auth_challenge(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        ChallengeName="NEW_PASSWORD_REQUIRED",
        Session=session,
        ChallengeResponses={
            "USERNAME": username,
            "NEW_PASSWORD": new_password,
            "SECRET_HASH": generate_secret_hash(username),
        },
    )

    result = response.get("AuthenticationResult")

    if not result:
        raise AuthenticationError(
            message="Password change could not be completed.",
        )

    return result




@handle_cognito_exceptions
def refresh_access_token(
    email: str,
    refresh_token: str,
):
    username = email

    response = cognito.initiate_auth(
        ClientId=settings.COGNITO_APP_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "USERNAME": username,
            "REFRESH_TOKEN": refresh_token,
            "SECRET_HASH": generate_secret_hash(username),
        },
    )

    result = response.get("AuthenticationResult")

    if not result:
        raise AuthenticationError(
            message="Token refresh could not be completed.",
        )

    return result

