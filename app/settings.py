from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class Env(str, Enum):
    """Окружения."""

    LOCAL = 'LOCAL'
    PROD = 'PROD'
    TEST = 'TEST'


class Settings(BaseSettings):
    """Настройки проекта."""

    ENV: Env = Env.LOCAL
    REDIS_HOST: str = 'redis://redis:6379/1'
    BASE_DIR: Path = Path().cwd()
    API: str = 'https://api.finex-etf.ru/v1'
    SENTRY_DSN: Optional[str] = None

    # Pg дефолтные значения нужны для работы alembic
    PG_HOST: str = 'localhost'
    PG_DB: str = 'calc_db_robo'
    PG_USER: str = 'calc_db_robo'
    PG_PASSWORD: str = 'calc_db_robo'
    PG_PORT: int = 5432

    OPENAPI_URL: str = '/openapi.json'

    @property
    def pg_dsn(self) -> str:
        """postgres_dsn.

        example: postgres://user:pass@localhost:5432/foobar
        """
        return 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
            user=self.PG_USER,
            password=self.PG_PASSWORD,
            host=self.PG_HOST,
            port=self.PG_PORT,
            db=self.PG_DB if self.ENV != Env.TEST else f'test_{self.PG_DB}',
        )


conf = Settings()
