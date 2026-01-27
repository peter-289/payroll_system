from sqlalchemy.orm import Session
from app.models.audit_model import AuditLog
from typing import List
import json


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log_action(self, user_id: int, action: str, metadata: dict = None) -> AuditLog:
        metadata_str = json.dumps(metadata) if metadata else None
        log = AuditLog(user_id=user_id, action=action, metadata=metadata_str)
        self.db.add(log)
        
        return log

    def get_all_logs(self) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

    def delete_log(self, log_id: int) -> None:
        log = self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
        if log:
            self.db.delete(log)
    
    def delete_all_logs(self) -> None:
        self.db.query(AuditLog).delete()