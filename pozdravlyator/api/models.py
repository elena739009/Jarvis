import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from .database import Base
from .config import settings


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _expires():
    return _utcnow() + timedelta(hours=settings.job_ttl_hours)


class Job(Base):
    __tablename__ = "jobs"

    id            = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status        = Column(String(20), nullable=False, default="pending")
    # pending | processing | done | error

    text          = Column(String(500), nullable=False)
    mode          = Column(String(10),  nullable=False, default="scrolling")
    watermark     = Column(Boolean,     nullable=False, default=True)

    photos_dir    = Column(String,  nullable=True)
    audio_path    = Column(String,  nullable=True)
    output_path   = Column(String,  nullable=True)
    error_message = Column(String,  nullable=True)

    ip_address    = Column(String(50), nullable=True)
    created_at    = Column(DateTime, nullable=False, default=_utcnow)
    expires_at    = Column(DateTime, nullable=False, default=_expires)
