
from functools import wraps

from botocore.exceptions import ClientError

from app.modules.auth.cognito_errors import handle_cognito_error


def handle_cognito_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ClientError as error:
            handle_cognito_error(error)

    return wrapper
