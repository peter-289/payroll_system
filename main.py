from fastapi import FastAPI
from backend.database_setups.initialize_db import init_db
from scripts.rbac_ import seed_role_permissions,  seed_roles, seed_permissions, seed_departments, seed_positions

from scripts.create_admin import seed_admin
from backend.database_setups.database_setup import SessionLocal
from backend.routes.department_routes import router as department_router
from backend.routes.tax_routes import router as tax_router
from backend.routes.user_routes import router as user_router
from backend.routes.auth_routes import router as auth_router
from backend.routes.attendance_routes import router as attendance_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Payroll System API, server is running!"}

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



# Register routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(attendance_router)
app.include_router(department_router)
app.include_router(tax_router)