from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class TextMode(str, Enum):
    scrolling = "scrolling"
    card      = "card"


class JobStatus(str, Enum):
    pending    = "pending"
    processing = "processing"
    done       = "done"
    error      = "error"


class JobResponse(BaseModel):
    id:            str
    status:        JobStatus
    text:          str
    mode:          TextMode
    watermark:     bool
    output_url:    Optional[str]  = None
    error_message: Optional[str]  = None
    created_at:    datetime
    expires_at:    datetime

    model_config = {"from_attributes": True}
