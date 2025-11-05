from datetime import date
from backend.models.payroll_model import Payroll
from backend.models.employee_model import Employee
from backend.models.department_model import Department
from backend.models.allowances_model import Allowance
from backend.models.deductions_model import Deduction
from backend.models.pension_model import Pension
from backend.database_setups.database_setup import SessionLocal
import decimal
import os


def _department_salary_band(dept_name: str) -> float:
    """Return salary band modifier or allowances based on department name."""
    bands = {
        'Engineering': 1.15,
        'HR': 1.05,
        'Finance': 1.10,
    }
    return bands.get(dept_name, 1.07)  # default multiplier


def _tax_for_income(gross: float) -> float:
    """Simple progressive tax for demonstration.

    Brackets:
    - up to 1000: 10%
    - 1000-3000: 15%
    - >3000: 20%
    """
    if gross <= 1000:
        return gross * 0.10
    if gross <= 3000:
        return 1000 * 0.10 + (gross - 1000) * 0.15
    return 1000 * 0.10 + 2000 * 0.15 + (gross - 3000) * 0.20


def _other_deductions(gross: float) -> float:
    """Other fixed deductions (pension, insurance) as a percent of gross."""
    pension = gross * 0.05
    insurance = gross * 0.02
    return pension + insurance


def generate_payslip_for_employee(employee_id: int, start: date, end: date, session=None) -> Payroll:
    """Generate a payroll entry (payslip) for an employee for the given period.

    Returns the created Payroll instance.
    """
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    try:
        emp = session.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise ValueError("Employee not found")

        basic = float(emp.salary_type or 0.0)
        dept_name = emp.department.name if emp.department else None

        # Department multiplier adds allowances implicitly
        multiplier = _department_salary_band(dept_name or '')
        dept_allowance_amt = round(basic * (multiplier - 1.0), 2)
        gross = round(basic + dept_allowance_amt, 2)

        # Base tax and other computed deductions
        tax_amt = round(_tax_for_income(gross), 2)

        # Pension contributions: if employee has pension settings, use those percentages
        pension_amt = 0.0
        pension = session.query(Pension).filter(Pension.employee_id == emp.employee_id).first()
        if pension and pension.employee_contribution_percentage:
            pension_amt = round(gross * (pension.employee_contribution_percentage / 100.0), 2)

        # Insurance / other fixed deductions
        insurance_amt = round(gross * 0.02, 2)

        # Total deductions and net
        total_deductions = round(tax_amt + pension_amt + insurance_amt, 2)
        net = round(gross - total_deductions, 2)

        # Create payroll row
        payroll = Payroll(
            employee_id=emp.employee_id,
            pay_period_start=start,
            pay_period_end=end,
            basic_salary=basic,
            gross_salary=gross,
            total_deductions=total_deductions,
            net_salary=net,
            payment_date=end,
            status='Generated'
        )
        session.add(payroll)
        session.commit()
        session.refresh(payroll)

        # Create allowance rows (department allowance)
        allowances = []
        if dept_allowance_amt and dept_allowance_amt > 0:
            allowances.append(Allowance(payroll_id=payroll.payroll_id, name='Department Allowance', type='department', amount=dept_allowance_amt, description=f'{dept_name} band allowance'))

        # Create deduction rows (tax, pension, insurance)
        deductions = []
        if tax_amt > 0:
            deductions.append(Deduction(payroll_id=payroll.payroll_id, name='Income Tax', type='tax', amount=tax_amt, description='Withholding tax'))
        if pension_amt > 0:
            deductions.append(Deduction(payroll_id=payroll.payroll_id, name='Pension (employee)', type='pension', amount=pension_amt, description='Employee pension contribution'))
        if insurance_amt > 0:
            deductions.append(Deduction(payroll_id=payroll.payroll_id, name='Insurance', type='insurance', amount=insurance_amt, description='Mandatory insurance deductions'))

        if allowances:
            session.add_all(allowances)
        if deductions:
            session.add_all(deductions)
        session.commit()
        # refresh payroll to load relationships
        session.refresh(payroll)
        return payroll
    finally:
        if close_session:
            session.close()


def render_payslip_text(payroll: Payroll) -> str:
    emp = payroll.employee
    lines = []
    lines.append(f"Payslip ID: {payroll.payroll_id}")
    lines.append(f"Employee: {emp.first_name} {emp.last_name} (ID: {emp.employee_id})")
    lines.append(f"Period: {payroll.pay_period_start} to {payroll.pay_period_end}")
    lines.append("")
    lines.append(f"Basic Salary: {payroll.basic_salary:.2f}")
    lines.append(f"Gross Salary: {payroll.gross_salary:.2f}")
    lines.append("")
    # Allowances
    lines.append("Allowances:")
    total_allowances = 0.0
    if hasattr(payroll, 'allowances') and payroll.allowances:
        for a in payroll.allowances:
            amt = float(a.amount or 0.0)
            total_allowances += amt
            lines.append(f" - {a.name}: {amt:.2f} ({a.type})")
    else:
        lines.append(" - None")
    lines.append(f"Total Allowances: {total_allowances:.2f}")

    # Deductions
    lines.append("")
    lines.append("Deductions:")
    total_deductions = 0.0
    if hasattr(payroll, 'deductions') and payroll.deductions:
        for d in payroll.deductions:
            amt = float(d.amount or 0.0)
            total_deductions += amt
            lines.append(f" - {d.name}: {amt:.2f} ({d.type})")
    else:
        lines.append(" - None")
    lines.append(f"Total Deductions: {total_deductions:.2f}")

    # Totals
    lines.append("")
    lines.append(f"Net Salary: {payroll.net_salary:.2f}")
    lines.append("")
    lines.append("Breakdown:")
    lines.append(f" - Generated on: {payroll.created_at if hasattr(payroll, 'created_at') else ''}")
    return "\n".join(lines)


def save_payslip_to_file(payroll: Payroll, dest_dir: str = None) -> str:
    if dest_dir is None:
        dest_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'tmp')
    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.join(dest_dir, f"payslip_{payroll.payroll_id}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(render_payslip_text(payroll))
    return filename
