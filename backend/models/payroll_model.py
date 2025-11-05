from datetime import datetime
from backend.database_setups.database_setup import Base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship

class Payroll(Base):
    __tablename__ = "payrolls"
    
    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    basic_salary = Column(Float, nullable=False)  # Position's base salary
    department_multiplier = Column(Float, nullable=False, default=1.0)  # Salary multiplier from department
    position_grade_multiplier = Column(Float, nullable=False, default=1.0)  # Multiplier based on position grade
    adjusted_base_salary = Column(Float, nullable=False)  # Basic salary after applying multipliers
    allowances_breakdown = Column(JSON)  # Detailed breakdown of allowances
    deductions_breakdown = Column(JSON)  # Detailed breakdown of deductions
    gross_salary = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # e.g., Paid, Pending, Failed
    bank_transaction_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    employee = relationship("Employee", back_populates="payrolls")  
    allowances = relationship("Allowance", back_populates="payroll")
    deductions = relationship("Deduction", back_populates="payroll")
    
    @property
    def grade_multipliers(self):
        """Standard multipliers for different pay grades"""
        return {
            'Entry': 1.0,
            'Junior': 1.2,
            'Mid': 1.5,
            'Senior': 1.8,
            'Lead': 2.1,
            'Manager': 2.5,
            'Director': 3.0
        }

    def calculate_salary(self):
        """Calculate the complete salary breakdown"""
        # Get employee's position and department
        position = self.employee.position
        department = position.department if position else None
        
        # Set base salary from position
        self.basic_salary = position.base_salary if position else 0
        
        # Apply department multiplier
        self.department_multiplier = department.salary_multiplier if department else 1.0
        
        # Apply position grade multiplier
        self.position_grade_multiplier = self.grade_multipliers.get(position.pay_grade, 1.0) if position else 1.0
        
        # Calculate adjusted base salary
        self.adjusted_base_salary = (
            self.basic_salary * 
            self.department_multiplier * 
            self.position_grade_multiplier
        )
        
        # Calculate allowances
        allowances_total = 0
        self.allowances_breakdown = {}
        
        for allowance in self.allowances:
            amount = allowance.amount
            self.allowances_breakdown[allowance.allowance_type] = amount
            allowances_total += amount
        
        # Calculate deductions
        deductions_total = 0
        self.deductions_breakdown = {}
        
        for deduction in self.deductions:
            amount = deduction.amount
            self.deductions_breakdown[deduction.deduction_type] = amount
            deductions_total += amount
        
        # Calculate final amounts
        self.gross_salary = self.adjusted_base_salary + allowances_total
        self.total_deductions = deductions_total
        self.net_salary = self.gross_salary - self.total_deductions
        
        return {
            'basic_salary': self.basic_salary,
            'department_multiplier': self.department_multiplier,
            'position_grade_multiplier': self.position_grade_multiplier,
            'adjusted_base_salary': self.adjusted_base_salary,
            'allowances': self.allowances_breakdown,
            'deductions': self.deductions_breakdown,
            'gross_salary': self.gross_salary,
            'total_deductions': self.total_deductions,
            'net_salary': self.net_salary
        }
