from sqlalchemy.orm import Session
from app.services.deduction_service import DeductionService
from app.services.salary_service import SalaryService
from app.services.tax_service import TaxService
from app.services.allowance_type_service import AllowanceTypeService
from app.services.attendance_service import AttendanceService
from app.services.loan_service import LoanService
from app.services.insurance_service import InsuranceService
from app.services.pension_service import PensionService
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService
from datetime import date
from app.schemas.payroll_schema import ResolvedPayrollInputs



class PayrollResolutionService:
    def __init__(self, db: Session):
        self.db = db
        self.deduction_service = DeductionService(db)
        self.salary_service = SalaryService(db)
        self.tax_service = TaxService(db)
        self.allowance_service = AllowanceTypeService(db)
        self.attendance_service = AttendanceService(db)
        self.loan_service = LoanService(db)
        self.insurance_service = InsuranceService(db)
        self.pension_service = PensionService(db)
        self.department_service = DepartmentService(db)
        self.user_service = EmployeeService(db)

    def get_employee(self, employee_id:int):
        employee = self.user_service.get_employee_by_id(employee_id)
        return employee

    def get_base_salary(self, employee_id: int):
        salary = self.salary_service.get_employee_salary(employee_id)
        return salary.amount
    
    def get_deduction_details(self, deduction_id: int):
        deduction = self.deduction_service.get_deduction(deduction_id)
        return deduction
    
    def get_current_position_salary(self, position_id:int):
        position_salary = self.salary_service.get_current_position_salary(position_id)
        return position_salary.amount
    
    def get_tax_details(self, tax_id: int):
        tax = self.tax_service.get_tax_rule(tax_id)
        return tax
    
    def get_fixed_tax(self, tax_id:int):
        fixed_taxes = self.tax_service.get_fixed_tax_rules(tax_id)
        return fixed_taxes.max_annual_tax
    
    def get_allowance_type(self, allowance_type_id:int):
        allowance_type = self.allowance_service.get_allowance_type(allowance_type_id)
        return allowance_type
    
    def get_insurance_details(self, employee_id:int):
        insurance = self.insurance_service.get_employee_policy(employee_id)
        return insurance
    
    def get_loan_details(self, employee_id:int):
        loan = self.loan_service.get_employee_loan(employee_id)
        return loan
    
    def get_attendance(self, employee_id:int):
        attendance = self.attendance_service.get_employee_attendance(employee_id)
        return attendance
    
    def get_pension_details(self, employee_id:int):
        pension = self.pension_service.get_employee_pension(employee_id)
        return pension
    
    def get_position(self, employee_id:int):
        position = self.user_service.get_employee_position(employee_id)
        return position
    
    def get_department_details(self, employee_id:int):
        department = self.user_service.get_employee_department(employee_id)
        return department
    
#=============================================================================================
# ------------ Resolve payroll inputs --------------------------------------------------------
    def resolve_payroll_inputs(
            self,
            employee_id:int,
            allowance_type_id:int,
            tax_id:int,
            period_start:date,
            period_end:date
    )->ResolvedPayrollInputs:
        employee = self.get_employee(employee_id)
        base_salary = self.get_base_salary(employee_id)

        if base_salary is None:
            position = self.get_position(employee_id)
            base_salary = self.get_current_position_salary(position.id)
        
        allowances = self.get_allowance_type(allowance_type_id)
        tax_brackets = self.get_tax_details(tax_id)
        attendance = self.get_attendance(employee_id)
        loans = self.get_loan_details(employee_id)
        insurance = self.get_insurance_details(employee_id)
        pension = self.get_pension_details(employee_id)
        
        return ResolvedPayrollInputs(
        employee=employee.id,
        base_salary=base_salary,
        allowances=allowances,
        tax_brackets=tax_brackets,
        hours_worked=attendance.hours_worked,
        overtime_hours=attendance.overtime_hours,
        loans=loans,
        insurance_contribution=insurance.employee_contribution,
        pension_contribution=pension.monthly_contribution,
        period_start=period_start,
        period_end=period_end
    )