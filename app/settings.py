from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, BaseSettings, HttpUrl, PostgresDsn, RedisDsn, validator

DEFAULT_POSTGRES_PORT = '5432'


class RedisSettings(BaseSettings):
    """Setup redis."""

    REDIS_HOST: Optional[str] = None
    REDIS_USER: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: Optional[str] = None
    REDIS_URI: Optional[RedisDsn] = None

    @validator('REDIS_URI', pre=True)
    def build_redis_dsn(cls, redis_dsn: Optional[str], values: Dict[str, Any]) -> Any:  # noqa: N805
        """Set REDIS_URI."""
        if values.get('REDIS_HOST'):
            return RedisDsn.build(
                scheme='redis',
                user=values.get('REDIS_USER'),
                password=values.get('REDIS_PASSWORD'),
                host=values.get('REDIS_HOST'),
                port=values.get('REDIS_PORT'),
                path=values.get('REDIS_DB'),
            )
        return None


class DbSettings(BaseSettings):
    """Setup database."""

    # POSTGRES default values need for alembic
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_PORT: str = DEFAULT_POSTGRES_PORT
    POSTGRES_URI: Optional[PostgresDsn]
    POSTGRES_POOL_MIN: Optional[int] = 10
    POSTGRES_POOL_MAX: Optional[int] = 20

    @validator('POSTGRES_URI', pre=True)
    def build_pg_dsn(cls, val: Optional[str], values: Dict[str, Any]) -> Any:  # noqa: N805
        """Set POSTGRES_URI."""
        if isinstance(val, str):
            return val
        db = f'/{values.get("POSTGRES_DB")}'
        if db and values.get('ENV') == 'TEST':
            db = f'{db}_test'
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=db,
        )


class Settings(BaseSettings):
    """Настройки проекта."""

    ENV: Optional[str] = None
    BASE_DIR: Path = Path().cwd()
    SENTRY_DSN: Optional[HttpUrl] = None
    ROOT_PATH: str = '/'
    PROJECT_NAME: str = '*'
    PROJECT_DESCRIPTION: str = '*'
    PROJECT_VERSION: str = '*'

    redis: RedisSettings = RedisSettings()
    postgres: DbSettings = DbSettings()

    @validator('SENTRY_DSN', pre=True)
    def build_sentry_dsn(cls, sentry_dsn: Optional[str], values: Dict[str, Any]) -> Any:  # noqa: N805
        """Set SENTRY_DSN."""
        if sentry_dsn:
            return HttpUrl(sentry_dsn)
        return None


conf = Settings()
