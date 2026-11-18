
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import verify_cognito_token
from app.database.session import get_db
from app.modules.user import repository
from app.modules.user.models import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Verify Cognito token and retrieve the active PostgreSQL user."""

    # Verify Cognito access token.
    try:
        payload = verify_cognito_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        ) from exc

    # Extract Cognito user ID.
    cognito_sub = payload.get("sub")

    if not cognito_sub:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token: user ID is missing",
        )

    # Retrieve user from PostgreSQL.
    user = repository.get_user_by_cognito_sub(
        db=db,
        cognito_sub=cognito_sub,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    return user
