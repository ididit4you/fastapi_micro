from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator

DEFAULT_POSTGRES_PORT = '5432'


class RedisSettings(BaseSettings):
    """Setup redis."""

    REDIS_HOST: str = 'localhost'
    REDIS_USER: Optional[str] = None
    REDIS_PORT: str = '6379'
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: str = '/10'
    REDIS_URI: Optional[RedisDsn] = None

    @validator('REDIS_URI', pre=True)
    def build_redis_dsn(cls, redis_dsn: Optional[str], values: Dict[str, Any]) -> Any:  # noqa: N805
        """Set REDIS_URI."""
        if redis_dsn:
            return redis_dsn
        return RedisDsn.build(
            scheme='redis',
            user=values.get('REDIS_USER'),
            password=values.get('REDIS_PASSWORD'),
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            path=values.get('REDIS_DB'),
        )


class DbSettings(BaseSettings):
    """Setup database."""

    # POSTGRES default values need for alembic
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_PORT: str = DEFAULT_POSTGRES_PORT
    POSTGRES_URI: Optional[PostgresDsn] = None
    POSTGRES_POOL_MIN: int = 1
    POSTGRES_POOL_MAX: int = 10

    @validator('POSTGRES_URI', pre=True)
    def build_pg_dsn(cls, pg_dsn: Optional[str], values: Dict[str, Any]) -> Any:  # noqa: N805
        """Set POSTGRES_URI."""
        if pg_dsn:
            return pg_dsn
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path='/{db}'.format(db=values.get('POSTGRES_DB')),
        )


class Settings(BaseSettings):
    """Настройки проекта."""

    BASE_DIR: Path = Path().cwd()
    SENTRY_DSN: Optional[str] = None
    ROOT_PATH: str = '/'
    PROJECT_NAME: str = '*'
    PROJECT_DESCRIPTION: str = '*'
    PROJECT_VERSION: str = '*'

    redis: RedisSettings = RedisSettings()
    postgres: DbSettings = DbSettings()


conf = Settings()
