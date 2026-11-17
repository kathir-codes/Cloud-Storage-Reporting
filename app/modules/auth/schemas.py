
from pydantic import BaseModel, EmailStr, Field, field_validator


# Reusable email normalization
class EmailRequestMixin(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        if isinstance(value, str):
            return value.strip().lower()

        return value


# Login request
class LoginRequest(EmailRequestMixin):
    password: str = Field(min_length=8)


# First-time password change request
class CompleteNewPasswordRequest(EmailRequestMixin):
    session: str = Field(min_length=1)
    new_password: str = Field(min_length=8)


# Refresh token request
class RefreshTokenRequest(EmailRequestMixin):
    refresh_token: str = Field(min_length=1)


# Successful login response
class LoginSuccessResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int


# First-time password challenge response
class PasswordChallengeResponse(BaseModel):
    challenge_name: str
    session: str


# Authentication token response
class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int
