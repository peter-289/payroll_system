from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.initialize_db import init_db
from scripts.seed_utility import seed_role_permissions,seed_salaries, seed_roles, seed_permissions, seed_departments, seed_positions
from scripts.create_admin import seed_admin
from app.db.database_setup import SessionLocal

# Import all routers
from app.api.v1.department_routes import router as department_router
from app.api.v1.tax_routes import router as tax_router
from app.api.v1.user_routes import router as user_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.attendance_routes import router as attendance_router
from app.api.v1.allowance_type_routes import router as allowance_type_router
from app.api.v1.insuarance_routes import router as insurance_router
from app.api.v1.allowance_routes import router as allowance_router
from app.api.v1.payroll_routes import router as payroll_router
from app.api.v1.salary_routes import router as salary_router
from app.api.v1.deduction_routes import router as deduction_router
from app.api.v1.pension_routes import router as pension_router
from app.api.v1.loan_routes import router as loan_router
#from backend.routes.payroll_routes import router as payroll_router
#from backend.routes.deduction_routes import router as deduction_router
#from backend.routes.employee_routes import router as employee_router

app = FastAPI(
    title="Payroll System API",
    description="Comprehensive payroll management system with Swagger documentation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Payroll System API",
        "status": "Running",
        "documentation": "/docs",
        "endpoints": {
            "employees": "/employees",
            "payroll_compute_by_employee": "/api/v1/employees/{id}/payrolls/compute",
            "payroll_compute": "/api/v1/payrolls/compute",
            "deductions": "/deductions",
            "allowances": "/allowances",
            "taxes": "/taxes",
            "departments": "/departments",
            "users": "/users",
            "auth": "/auth",
            "salaries": "/employees/{id}/salary",
            "pensions": "/pensions",
            "loans": "/loans"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    init_db()
    seed_admin(db)
    seed_roles(db)
    seed_permissions(db)
    seed_role_permissions(db)
    seed_departments(db)
    seed_positions(db)
    seed_salaries(db)
    db.close()


# Register all routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(attendance_router)
app.include_router(department_router)
app.include_router(tax_router)
app.include_router(allowance_type_router)
app.include_router(insurance_router)
app.include_router(allowance_router)
#app.include_router(employee_router)
app.include_router(deduction_router)
app.include_router(salary_router)
app.include_router(pension_router)
app.include_router(loan_router)
app.include_router(payroll_router)