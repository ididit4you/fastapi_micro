from alembic import command
from alembic.config import Config


def mm() -> None:
    """Migrate."""
    config = Config('alembic.ini')   # Run the migrations.
    command.upgrade(config, 'head')


if __name__ == '__main__':
    mm()
