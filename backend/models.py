from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.types import JSON
from typing import Optional, List
from datetime import datetime

class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service: str = Field(index=True)
    name: str
    key_value: str
    metadata_json: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_checked: Optional[datetime] = None
    checks: List["HealthCheck"] = Relationship(back_populates="api_key")

class HealthCheck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    api_key_id: int = Field(foreign_key="apikey.id")
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    status: str
    response_time_ms: float
    error_message: Optional[str] = None

    api_key: Optional[APIKey] = Relationship(back_populates="checks")
