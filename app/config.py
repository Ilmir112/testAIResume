import os
from typing import Literal

from pydantic import ConfigDict, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEV", "TEST", "PROD", "INFO"]
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@"
            f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    HAWK_DSN: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = ConfigDict(env_file=".env")


try:
    settings = Settings()
    print(settings.TEST_DATABASE_URL)
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
    print(e)
