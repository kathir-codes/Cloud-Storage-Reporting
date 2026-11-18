
from sqlalchemy.orm import Session

from app.modules.user.models import User


def get_user_by_cognito_sub(
    db: Session,
    cognito_sub: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.cognito_sub == cognito_sub)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    cognito_sub: str,
    email: str,
    name: str | None = None,
) -> User:
    user = User(
        cognito_sub=cognito_sub,
        email=email,
        name=name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
