from pydantic import BaseModel, EmailStr, field_validator

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_max_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password must be 72 bytes or fewer")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_max_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password must be 72 bytes or fewer")
        return value

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
