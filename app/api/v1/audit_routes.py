from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.repositories.audit_repo import AuditRepository
from app.core.security import admin_access
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.services.audit_service import AuditService
from app.core.unit_of_work import UnitOfWork


# Get service
def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    uow = UnitOfWork(db)
    return AuditService(uow)

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime
    meta_data: str | None = None
    

    class Config:
        from_attributes = True


router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/logs", response_model=List[AuditLogResponse])
def get_audit_log(
    service: AuditService = Depends(get_audit_service),
    _current=Depends(admin_access)
):
    logs = service.get_audit_logs()
    return logs

@router.delete("/logs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(
    log_id: int,
    service: AuditService = Depends(get_audit_service),
    _current=Depends(admin_access)
):
    service.delete_audit_log(log_id)