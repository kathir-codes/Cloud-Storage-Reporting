
from fastapi import APIRouter

from app.modules.auth.schemas import (
    CompleteNewPasswordRequest,
    LoginRequest,
    LoginSuccessResponse,
    PasswordChallengeResponse,
    RefreshTokenRequest,
    TokenResponse,
)

from app.modules.auth.service import (
    complete_new_password,
    login_user,
    refresh_access_token,
)


router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    response_model=LoginSuccessResponse | PasswordChallengeResponse,
)

def login(payload: LoginRequest):
    result = login_user(
        email=payload.email,
        password=payload.password,
    )

    if result.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        return PasswordChallengeResponse(
            challenge_name=result["ChallengeName"],
            session=result["Session"],
        )

    return LoginSuccessResponse(
        access_token=result["AccessToken"],
        id_token=result["IdToken"],
        refresh_token=result.get("RefreshToken"),
        token_type=result["TokenType"],
        expires_in=result["ExpiresIn"],
    )


@router.post(
    "/complete-new-password",
    response_model=TokenResponse,
)
def complete_password(payload: CompleteNewPasswordRequest):
    result = complete_new_password(
        email=payload.email,
        session=payload.session,
        new_password=payload.new_password,
    )

    return {
        "access_token": result["AccessToken"],
        "id_token": result["IdToken"],
        "refresh_token": result.get("RefreshToken"),
        "token_type": result["TokenType"],
        "expires_in": result["ExpiresIn"],
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest):
    result = refresh_access_token(
        email=payload.email,
        refresh_token=payload.refresh_token,
    )

    return {
        "access_token": result["AccessToken"],
        "id_token": result["IdToken"],
        "refresh_token": result.get("RefreshToken"),
        "token_type": result["TokenType"],
        "expires_in": result["ExpiresIn"],
    }
