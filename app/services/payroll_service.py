"""Compatibility module exposing payroll engine and resolution helpers as `payroll_service`."""
import warnings
from app.services.payroll_engine import PayrollEngine, GrossPayInput, ComputeError
from app.services.payroll_resolution_service import PayrollResolutionService

warnings.warn(
    "app.services.payroll_service is a compatibility wrapper; prefer using PayrollEngine or PayrollResolutionService directly",
    DeprecationWarning,
)

__all__ = ["PayrollEngine", "GrossPayInput", "ComputeError", "PayrollResolutionService"]


# New PayrollService
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.repositories.audit_repo import AuditRepository
from app.payroll.payroll_engine import PayrollEngine
from app.schemas.payroll_schema import PayrollRunRequest, PayrollRunResponse
from app.domain.exceptions.base import PayrollComputeError
from typing import List
from app.models.payroll_model import Payroll, PayrollStatus
from datetime import date


class PayrollService:
    def __init__(self, db: Session):
        self.db = db
        self.payroll_repo = PayrollRepository(db)
        self.engine = PayrollEngine()
        self.audit_repo = AuditRepository(db)

    def run_payroll(self, request: PayrollRunRequest, user_id: int) -> PayrollRunResponse:
        """
        Run payroll for an employee and persist the record.
        """
        # TODO: Resolve full inputs, but for now use simple
        # For simplicity, assume request has enough data, but actually need to fetch employee data

        # Placeholder: create a dummy PayrollInput
        from app.schemas.payroll_schema import PayrollInput, EarningItem, DeductionItem, AllowanceItem

        # Fetch employee salary, etc. - but for now, assume provided
        payload = PayrollInput(
            employee_id=request.employee_id,
            period_start=request.pay_period_start,
            period_end=request.pay_period_end,
            earnings=[EarningItem(code="BASE", amount=50000.0, taxable=True)],  # dummy
            deductions=[],
            allowances=[]
        )

        # Compute
        result = self.engine.compute_simple(payload)

        # Persist
        payroll = Payroll(
            employee_id=request.employee_id,
            pay_period_start=request.pay_period_start,
            pay_period_end=request.pay_period_end,
            payment_date=date.today(),  # TODO: calculate
            total_allowances=result.allowances_total,
            total_deductions=result.deductions_total,
            tax_amount=result.tax_total,
            gross_salary=result.gross_pay,
            net_salary=result.net_pay,
            status=PayrollStatus.PROCESSED
        )

        self.payroll_repo.create(payroll)

        # Log action
        self.audit_repo.log_action(user_id, "payroll_run", {"payroll_id": payroll.id, "employee_id": request.employee_id})

        return PayrollRunResponse(
            id=payroll.id,
            employee_id=payroll.employee_id,
            pay_period_start=payroll.pay_period_start,
            pay_period_end=payroll.pay_period_end,
            payment_date=payroll.payment_date,
            gross_salary=payroll.gross_salary,
            net_salary=payroll.net_salary,
            status=payroll.status.value
        )

    def get_payroll_by_id(self, payroll_id: int) -> Payroll:
        return self.payroll_repo.get_by_id(payroll_id)

    def get_employee_payrolls(self, employee_id: int) -> List[Payroll]:
        return self.payroll_repo.get_by_employee(employee_id)
