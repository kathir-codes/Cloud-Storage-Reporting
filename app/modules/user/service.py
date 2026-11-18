
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.modules.user import repository


def sync_cognito_user(
    db: Session,
    cognito_sub: str,
    email: str,
    name: str | None = None,
):
    user = repository.get_user_by_cognito_sub(
        db=db,
        cognito_sub=cognito_sub,
    )

    if user:
        return user

    # Avoid creating a second account with an existing email.
    existing_user = repository.get_user_by_email(
        db=db,
        email=email,
    )

    if existing_user:
        raise AuthenticationError(
            message="Email is already associated with another account.",
        )

    return repository.create_user(
        db=db,
        cognito_sub=cognito_sub,
        email=email,
        name=name,
    )
