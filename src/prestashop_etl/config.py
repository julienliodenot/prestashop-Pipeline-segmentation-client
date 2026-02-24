import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    extract_start_date: str
    extract_end_date: str
    sqlite_db_path: str


def load_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    config_env_path = project_root / "config" / ".env"
    root_env_path = project_root / ".env"

    if config_env_path.exists():
        load_dotenv(dotenv_path=config_env_path)
    elif root_env_path.exists():
        load_dotenv(dotenv_path=root_env_path)
    else:
        raise FileNotFoundError("fichier .env non trouvé")

    api_key = os.getenv("PRESTASHOP_API_KEY", "").strip()
    base_url = os.getenv("PRESTASHOP_BASE_URL", "").strip().rstrip("/")

    if not api_key or not base_url:
        raise ValueError("Missing PRESTASHOP_API_KEY or PRESTASHOP_BASE_URL in .env")

    return Settings(
        api_key=api_key,
        base_url=base_url,
        extract_start_date=os.getenv("EXTRACT_START_DATE", "2025-01-01"),
        extract_end_date=os.getenv("EXTRACT_END_DATE", "2026-01-01"),
        sqlite_db_path=os.getenv("SQLITE_DB_PATH", "data/raw/prestashop.db"),
    )
