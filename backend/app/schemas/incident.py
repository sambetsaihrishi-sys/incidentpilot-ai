from pydantic import BaseModel
from typing import Optional


class IncidentCreate(BaseModel):
    service: str
    status_code: int
    error_message: str
    endpoint: Optional[str] = None
    response_time_ms: Optional[int] = None
    severity: Optional[str] = None


class IncidentResolution(BaseModel):
    root_cause: str
    resolution: str
    resolution_time_minutes: int