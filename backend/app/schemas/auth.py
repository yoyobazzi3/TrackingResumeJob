"""Pydantic schemas for auth payloads and responses."""

from pydantic import BaseModel, EmailStr, field_validator, Field


class SignupRequest(BaseModel):
    # Signup input payload.
    email: EmailStr
    password: str

    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

    @field_validator("password")
    @classmethod
    def password_max_bytes(cls, value: str) -> str:
        # BCrypt only supports up to 72 bytes.
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password must be 72 bytes or fewer")
        return value


class LoginRequest(BaseModel):
    # Login input payload.
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_max_bytes(cls, value: str) -> str:
        # BCrypt only supports up to 72 bytes.
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password must be 72 bytes or fewer")
        return value


class TokenResponse(BaseModel):
    # JWT access token response.
    access_token: str
    token_type: str = "bearer"
