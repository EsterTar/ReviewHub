import os
from functools import lru_cache
from logging import config as logging_config

from pydantic_settings import BaseSettings

from utils.logger import LOGGING

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str
    app_host: str
    app_port: int

    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    mongodb_uri: str

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging_config.dictConfig(LOGGING)

    jwt_secret_key: str
    jwt_algorithm: str

    debug: bool
    sentry_dsn: str

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache(maxsize=None)
def get_settings():
    settings = Settings()
    return settings
