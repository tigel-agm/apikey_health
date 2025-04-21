from sqlmodel import Session, select
from fastapi import HTTPException
from .models import APIKey, HealthCheck
from typing import Optional

def create_api_key(session: Session, api_key: APIKey) -> APIKey:
    session.add(api_key)
    session.commit()
    session.refresh(api_key)
    return api_key


def get_api_keys(session: Session):
    return session.exec(select(APIKey)).all()


def get_api_key(session: Session, key_id: int) -> APIKey:
    api_key = session.get(APIKey, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return api_key


def delete_api_key(session: Session, key_id: int):
    api_key = get_api_key(session, key_id)
    session.delete(api_key)
    session.commit()
    return api_key


def create_health_check(session: Session, api_key_id: int, status: str, response_time_ms: float, error_message: Optional[str] = None):
    health = HealthCheck(api_key_id=api_key_id, status=status, response_time_ms=response_time_ms, error_message=error_message)
    session.add(health)
    session.commit()
    session.refresh(health)
    return health

def get_health_checks(session: Session, api_key_id: int):
    """Return health check logs for the specified API key."""
    return session.exec(
        select(HealthCheck)
        .where(HealthCheck.api_key_id == api_key_id)
        .order_by(HealthCheck.checked_at.desc())
    ).all()
