from typing import List
from sqlalchemy.orm import Session
from app.db.database_setup import get_db
from app.schemas.payroll_schema import PayrollRunRequest, PayrollRunResponse
from app.payroll.payroll_engine import PayrollEngine
from app.services.payroll_service import PayrollService
from app.domain.exceptions.base import EmployeeNotFoundError, PayrollEngineError
from app.core.security import get_current_employee, admin_hr_or_self
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import EmployeeService
from app.schemas.payroll_schema import PayrollInput, PayrollResult
from datetime import date
from app.domain.exceptions.base import PayrollComputeError

router = APIRouter(prefix="/api/v1", tags=["Payrolls"])


@router.post("/employees/{employee_id}/payrolls/compute", response_model=PayrollResult)
def compute_employee_payroll(
    employee_id: int,
    payload: PayrollInput,
    db: Session = Depends(get_db),
    _current=Depends(admin_hr_or_self),
):
    if employee_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID must be positive")

    try:
        employee_service = EmployeeService(db)
        employee = employee_service.get_employee_by_id(employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve employee")

    # Ensure the payload employee_id matches the path
    if payload.employee_id != employee_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload employee_id mismatch")

    engine = PayrollEngine()
    try:
        result = engine.compute_simple(payload)
        # attach minimal employee info to audit
        if result.audit is None:
            result.audit = {}
        result.audit["employee"] = {"id": employee.id, "user_id": employee.user_id}
        return result
    except PayrollEngineError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/payrolls/compute", response_model=PayrollResult)
def compute_payroll(payload: PayrollInput, db: Session = Depends(get_db), current_employee: dict = Depends(get_current_employee)):
    # Open compute endpoint: allow admin/hr or the employee themself
    try:
        # verify employee exists to provide minimal audit info
        employee_service = EmployeeService(db)
        employee = employee_service.get_employee_by_id(payload.employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve employee")

    # RBAC: allow admin/hr or owner
    role = current_employee.get("role")
    if role not in ("admin", "hr") and current_employee.get("employee_id") != payload.employee_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin/HR or owner access required")

    engine = PayrollEngine()
    try:
        result = engine.compute_simple(payload)
        if result.audit is None:
            result.audit = {}
        result.audit["employee"] = {"id": employee.id, "user_id": employee.user_id}
        result.audit["requested_by"] = {"user_id": current_employee.get("user_id"), "role": role}
        return result
    except PayrollEngineError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# --- Lightweight run endpoint that persists a Payroll record via PayrollService ---
@router.post("/payroll/run", response_model=PayrollRunResponse)
def run_payroll(payload: PayrollRunRequest, db: Session = Depends(get_db), current_employee: dict = Depends(get_current_employee)):
    try:
        service = PayrollService(db)
        payroll = service.run_payroll(payload, current_employee["user_id"])
        return payroll
    except PayrollComputeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/payroll/batch", response_model=List[PayrollRunResponse])
def run_batch_payroll(
    period_start: date,
    period_end: date,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    # Only admin or hr can run batch
    role = current_employee.get("role")
    if role not in ("admin", "hr"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin or HR access required")

    # Get all employees
    from app.repositories.employee_repo import EmployeeRepository
    employee_repo = EmployeeRepository(db)
    employees = employee_repo.get_all_employees()

    results = []
    for emp in employees:
        request = PayrollRunRequest(
            employee_id=emp.id,
            pay_period_start=period_start,
            pay_period_end=period_end
        )
        try:
            service = PayrollService(db)
            payroll = service.run_payroll(request, current_employee["user_id"])
            results.append(payroll)
        except Exception as e:
            # Log error, but continue
            pass

    return results