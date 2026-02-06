"""JWT decoding utilities."""

from jose import jwt, JWTError
from app.core.config import settings

def decode_access_token(token: str) -> dict | None:
    # Decode and validate a JWT. Returns None on failure.
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
