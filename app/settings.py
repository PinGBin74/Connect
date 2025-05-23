from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432
    DB_USER: str = "connect"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "connect_db"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    CACHE_HOST: str = "0.0.0.0"
    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    SENTRY_DSN: str = ""

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
        env_file = ".env.test" if os.getenv("PYTEST_CURRENT_TEST") else ".local.env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
