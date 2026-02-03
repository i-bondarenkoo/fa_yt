from pydantic_settings import BaseSettings
from pathlib import Path

# базовая директория где весь проект
BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    # путь к файлу с бд
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True
    # db_echo: bool = False


settings = Settings()
