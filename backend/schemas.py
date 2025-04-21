from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class APIKeyCreate(SQLModel):
    service: str
    name: str
    key_value: str
    metadata_json: Optional[dict] = Field(None, alias="metadata")

    class Config:
        validate_by_name = True

class APIKeyRead(SQLModel):
    id: int
    service: str
    name: str
    metadata_json: Optional[dict] = Field(None, alias="metadata")
    created_at: datetime
    last_checked: Optional[datetime] = None

    class Config:
        from_attributes = True
        validate_by_name = True

class HealthCheckRead(SQLModel):
    id: int
    api_key_id: int
    checked_at: datetime
    status: str
    response_time_ms: float
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
