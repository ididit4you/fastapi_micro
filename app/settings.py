from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, HttpUrl

DEFAULT_POSTGRES_PORT = '5432'


class Settings(BaseSettings):
    """Настройки проекта."""

    ENV: Optional[str] = None
    BASE_DIR: Path = Path().cwd()

    SENTRY_DSN: Optional[HttpUrl] = None
    ROOT_PATH: str = '/'
    PROJECT_NAME: str = '*'
    PROJECT_DESCRIPTION: str = '*'
    PROJECT_VERSION: str = '*'


conf = Settings()
