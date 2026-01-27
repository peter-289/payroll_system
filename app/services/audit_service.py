from app.core.unit_of_work import UnitOfWork
from datetime import datetime, date
from app.repositories.audit_repo import AuditRepository
from app.domain.exceptions.base import DomainError


class AuditService:
    """
    Service for handling audit logging within the attendance system.
    :param self: Refers to the AuditService instance
    :param uow: Unit of Work instance for managing database transactions
    :type uow: UnitOfWork
    :return: None
    :rtype: None
    """
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    def log_action(
            self, 
            user_id: int, 
            action: str, 
            metadata: str | None = None
        ) -> None:
        """
        Logs an action performed by a user.

        :param self: Refers to the AuditService instance
        :param user_id: An integer representing the unique identifier of the user
        :type user_id: int
        :param action: A string describing the action performed
        :type action: str
        :param meta_data: Optional string containing additional metadata about the action
        :type meta_data: str | None
        :return: None
        :rtype: None
        """
        with self.uow:
            self.uow.audit_repo.log_action(
                user_id=user_id,
                action=action,
                metadata=metadata
            )

    def get_audit_logs(self) -> list:
        """
        Retrieves all audit logs.

        :param self: Refers to the AuditService instance
        :return: A list of audit log entries
        :rtype: list
        """
        with self.uow:
            logs = self.uow.audit_repo.get_all_logs()
            return logs
    
    def delete_audit_log(self, log_id: int) -> None:
        """
        Deletes a specific audit log entry by its ID.

        :param self: Refers to the AuditService instance
        :param log_id: An integer representing the unique identifier of the audit log entry
        :type log_id: int
        :return: None
        :rtype: None
        """
        if log_id <= 0:
            raise DomainError("log_id must be a positive integer.")
        with self.uow:
            self.uow.audit_repo.delete_log(log_id)
        
    def delete_all_logs(self) -> None:
        """
        Deletes all audit log entries.

        :param self: Refers to the AuditService instance
        :return: None
        :rtype: None
        """
        with self.uow:
            self.uow.audit_repo.delete_all_logs()