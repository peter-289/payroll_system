from fastapi import FastAPI
from backend.database_setups.initialize_db import init_db
from scripts.rbac_ import seed_role_permissions, seed_roles, seed_permissions, seed_departments, seed_positions
from backend.routes import (
    auth_router,
    user_router,
    admin_router,
    email_router
)
from backend.database_setups.database_setup import SessionLocal

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Payroll System API, server is running!"}

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    init_db()
    seed_roles(db)
    seed_permissions(db)
    seed_role_permissions(db)
    seed_departments(db)
    seed_positions(db)
    db.close()



# Register routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(email_router)