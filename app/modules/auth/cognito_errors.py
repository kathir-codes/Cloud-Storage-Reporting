
import logging

from botocore.exceptions import ClientError

from app.core.exceptions import (
    AppException,
    AuthenticationError,
    ConflictError,
    ExternalServiceError,
)

logger = logging.getLogger(__name__)


def handle_cognito_error(error: ClientError) -> None:
    error_code = error.response.get("Error", {}).get("Code", "")

    if error_code == "UsernameExistsException":
        raise ConflictError(
            message="An account with this email already exists.",
            error_code="EMAIL_ALREADY_EXISTS",
        ) from error

    if error_code == "InvalidPasswordException":
        raise AppException(
            message="Password does not meet the password policy.",
            status_code=400,
            error_code="INVALID_PASSWORD",
        ) from error

    if error_code == "CodeMismatchException":
        raise AppException(
            message="Invalid confirmation code.",
            status_code=400,
            error_code="INVALID_CONFIRMATION_CODE",
        ) from error

    if error_code == "ExpiredCodeException":
        raise AppException(
            message="Confirmation code has expired.",
            status_code=400,
            error_code="CONFIRMATION_CODE_EXPIRED",
        ) from error

    if error_code in (
        "NotAuthorizedException",
        "UserNotFoundException",
    ):
        raise AuthenticationError(
            message="Invalid credentials or authentication failed.",
        ) from error

    if error_code == "UserNotConfirmedException":
        raise AppException(
            message="Please verify your email before signing in.",
            status_code=403,
            error_code="EMAIL_NOT_VERIFIED",
        ) from error

    if error_code == "LimitExceededException":
        raise AppException(
            message="Too many attempts. Please try again later.",
            status_code=429,
            error_code="TOO_MANY_ATTEMPTS",
        ) from error

    if error_code == "UserLambdaValidationException":
        raise AppException(
            message="The supplied user information could not be accepted.",
            status_code=400,
            error_code="USER_VALIDATION_FAILED",
        ) from error

    logger.error("Unexpected Cognito error: %s", error_code)

    raise ExternalServiceError(
        message="The authentication service is currently unavailable.",
    ) from error
