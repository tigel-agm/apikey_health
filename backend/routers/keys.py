from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..db import get_session, init_db
from ..schemas import APIKeyCreate, APIKeyRead, HealthCheckRead
from ..models import APIKey
from ..crud import create_api_key, get_api_keys, get_api_key, delete_api_key, create_health_check, get_health_checks
from ..adapters.openai_adapter import test_openai_key

router = APIRouter()

# Ensure DB tables exist
@router.on_event("startup")
def on_startup():
    init_db()

@router.post("/keys", response_model=APIKeyRead)
def add_key(key: APIKeyCreate, session: Session = Depends(get_session)):
    api_key_obj = APIKey(**key.model_dump())
    db_key = create_api_key(session, api_key_obj)
    # initial health check
    status, rt, err = test_openai_key(db_key.key_value)
    hc = create_health_check(session, db_key.id, status, rt, err)
    db_key.last_checked = hc.checked_at
    session.add(db_key)
    session.commit()
    session.refresh(db_key)
    return db_key

@router.get("/keys", response_model=List[APIKeyRead])
def list_keys(session: Session = Depends(get_session)):
    return get_api_keys(session)

@router.get("/keys/{key_id}", response_model=APIKeyRead)
def get_key(key_id: int, session: Session = Depends(get_session)):
    return get_api_key(session, key_id)

@router.delete("/keys/{key_id}", response_model=APIKeyRead)
def remove_key(key_id: int, session: Session = Depends(get_session)):
    return delete_api_key(session, key_id)

# Manual health check trigger
@router.post("/keys/{key_id}/checks/trigger", response_model=HealthCheckRead)
def trigger_check(key_id: int, session: Session = Depends(get_session)):
    api_key = get_api_key(session, key_id)
    status, rt, err = test_openai_key(api_key.key_value)
    hc = create_health_check(session, api_key.id, status, rt, err)
    api_key.last_checked = hc.checked_at
    session.add(api_key)
    session.commit()
    return hc

@router.get("/keys/{key_id}/checks", response_model=List[HealthCheckRead])
def list_checks(key_id: int, session: Session = Depends(get_session)):
    """Retrieve health check logs for a given API key."""
    return get_health_checks(session, key_id)
