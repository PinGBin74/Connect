from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432
    DB_USER: str = "connect"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "connect"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    CACHE_HOST: str = "0.0.0.0"
    OPENWEATHERMAPAPIKEY: str = ""
    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".local.env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
