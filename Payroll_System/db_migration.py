# migrate.py
import subprocess

def make_migration(message="auto migration"):
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])

def upgrade():
    subprocess.run(["alembic", "upgrade", "head"])

if __name__ == "__main__":
    # step 1: autogenerate migration
    make_migration("initial payroll tables")
    # step 2: apply migration
    upgrade()
