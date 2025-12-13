from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database_setups.initialize_db import init_db
from scripts.rbac_ import seed_role_permissions, seed_roles, seed_permissions, seed_departments, seed_positions
from scripts.create_admin import seed_admin
from backend.database_setups.database_setup import SessionLocal

# Import all routers
from backend.routes.department_routes import router as department_router
from backend.routes.tax_routes import router as tax_router
from backend.routes.user_routes import router as user_router
from backend.routes.auth_routes import router as auth_router
from backend.routes.attendance_routes import router as attendance_router
from backend.routes.allowance_type_routes import router as allowance_type_router
from backend.routes.insuarance_routes import router as insurance_router
from backend.routes.allowance_routes import router as allowance_router
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
            "payroll": "/payrolls",
            "deductions": "/deductions",
            "allowances": "/allowances",
            "taxes": "/taxes",
            "departments": "/departments",
            "users": "/users",
            "auth": "/auth"
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
#app.include_router(payroll_router)
#app.include_router(deduction_router)