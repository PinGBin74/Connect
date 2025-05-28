from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "connect"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "connect_db"
    DATABASE_URL: str = ""

    # Cache settings
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    CACHE_HOST: str = ""
    REDIS_URL: str = ""
    INTERNAL_REDIS_URL: str = ""

    # JWT settings
    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    SENTRY_DSN: str = ""

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://connect-bo5f.onrender.com",
    ]

    # Yandex Disk settings
    YANDEX_DISK_TOKEN: str = ""
    YANDEX_DISK_BASE_PATH: str = ""
    YANDEX_DISK_API_URL: str = ""
    YANDEX_DISK_UPLOAD_URL: str = ""
    YANDEX_DISK_PUBLISH_URL: str = ""
    YANDEX_DISK_INFO_URL: str = ""

    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""

    class Config:
        env_file = ".local.env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            # Remove sslmode parameter if present
            url = self.DATABASE_URL.split("?")[0]
            if self.DATABASE_URL.startswith("postgresql+asyncpg://"):
                return url
            return url.replace("postgresql://", "postgresql+asyncpg://")
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_url(self) -> str:
        if self.INTERNAL_REDIS_URL:
            return self.INTERNAL_REDIS_URL
        return self.REDIS_URL
