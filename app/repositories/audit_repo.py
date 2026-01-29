"""Repository for managing Audit Log entities in the database."""
from sqlalchemy.orm import Session
from app.models.audit_model import AuditLog
from typing import List
import json


class AuditRepository:
    """Repository for audit log database operations.
    
    Handles creation and retrieval of audit logs for tracking user actions
    and maintaining an immutable audit trail.
    """
    def __init__(self, db: Session):
        """Initialize the audit repository.
        
        Args:
            db: SQLAlchemy session for database operations.
        """
        self.db = db

    def log_action(self, user_id: int, action: str, metadata: dict = None) -> AuditLog:
        """Log a user action to the audit trail.
        
        Args:
            user_id: The ID of the user performing the action.
            action: Description of the action performed.
            metadata: Optional dictionary containing additional information about the action.
            
        Returns:
            The created AuditLog instance.
        """
        metadata_str = json.dumps(metadata) if metadata else None
        log = AuditLog(user_id=user_id, action=action, metadata=metadata_str)
        self.db.add(log)
        return log

    def get_all_logs(self) -> List[AuditLog]:
        """Retrieve all audit logs ordered by most recent first.
        
        Returns:
            List of all AuditLog instances in reverse chronological order.
        """
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

    def delete_log(self, log_id: int) -> None:
        """Delete a specific audit log by ID.
        
        Args:
            log_id: The ID of the audit log to delete.
        """
        log = self.db.query(AuditLog).filter(AuditLog.id == log_id).first()
        if log:
            self.db.delete(log)
    
    def delete_all_logs(self) -> None:
        """Delete all audit logs from the database.
        
        Warning: This permanently removes all audit trail records.
        """
        self.db.query(AuditLog).delete()