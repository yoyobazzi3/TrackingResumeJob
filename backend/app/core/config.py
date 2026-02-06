"""Application configuration loaded from environment."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database connection string.
    DATABASE_URL: str

    # Secret key for JWT signing.
    JWT_SECRET_KEY: str

    # JWT signing algorithm.
    JWT_ALGORITHM: str = "HS256"

    # Token lifetime in minutes.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
