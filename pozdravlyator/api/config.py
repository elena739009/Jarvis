# -*- coding: utf-8 -*-
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent   # pozdravlyator/


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{BASE_DIR / 'pozdravlyator.db'}"
    uploads_dir: str = str(BASE_DIR / "uploads")
    output_dir: str = str(BASE_DIR / "output")

    max_photos: int = 30
    max_photo_mb: int = 10
    max_audio_mb: int = 20
    jobs_per_hour_limit: int = 20
    job_ttl_hours: int = 24

    model_config = {"env_file": str(BASE_DIR / ".env"), "env_file_encoding": "utf-8"}


settings = Settings()
