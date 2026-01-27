"""Model package initializer.

Import model modules here so that SQLAlchemy mappers are configured
consistently when any model is imported. This avoids "failed to locate a
name" errors for string-based relationship targets when modules are
imported in different orders.
"""

# Import all model modules to ensure classes are registered with SQLAlchemy
from app.models import (
	insurance_model,
	allowances_model,
	deductions_model,
	department_model,
	employee_model,
	Loans_advances_model,
	payroll_model,
	pension_model,
	permissions_model,
	Position_model,
	roles_model,
	role_permission,
	tax_model,
	user_model,
)

__all__ = [
	"allowances_model",
	"deductions_model",
	"department_model",
	"employee_model",
	"insurance_model",
	"Loans_advances_model",
	"payroll_model",
	"pension_model",
	"permissions_model",
	"Position_model",
	"roles_model",
	"role_permission",
	"tax_model",
	"user_model",
]
