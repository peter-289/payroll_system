# Payroll System Backend

A comprehensive payroll management system backend built with FastAPI, SQLAlchemy, and other modern Python tools. Designed for local or LAN deployment with a Tkinter-based frontend client.

## Features

- User authentication and role-based access control (admin, hr, employee)
- Employee management
- Payroll computation with allowances, deductions, and taxes
- Payslip generation (PDF)
- Audit logging
- Batch payroll processing
- Secure password management

## Technology Stack

- **Web Framework**: FastAPI 0.115.0
- **Database & ORM**: SQLAlchemy 2.0.36
- **Authentication**: Python-JOSE, Passlib, Bcrypt
- **Data Validation**: Pydantic 2.9.2
- **Scheduling**: APScheduler 3.10.4
- **Reporting**: ReportLab 4.2.2, OpenPyXL 3.1.5, Pandas 2.2.3
- **Testing**: Pytest 8.3.2, HTTPX 0.27.2

## Project Structure

```
payroll_system/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Configuration, security, hashing
│   ├── db/              # Database setup and migrations
│   ├── domain/          # Business rules and exceptions
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic layer
│   └── payroll/         # Payroll computation logic
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.8+
- SQLite (default) or PostgreSQL/MySQL

### Setup

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./payroll.db
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=AdminPass123!
   ```

5. **Initialize the database**:
   ```bash
   python -m app.scripts.initialize_db
   ```

6. **Seed initial data**:
   ```bash
   python -m app.scripts.seed_utility
   ```

7. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Architecture

### Layer Responsibilities

- **Repository Layer**: Handles database access using SQLAlchemy ORM. Never commits/rolls back transactions or contains business logic.
- **Service Layer**: Orchestrates workflows, enforces business rules, calls repositories, uses Unit of Work for transactions.
- **API Layer**: Exposes FastAPI endpoints, handles authentication/RBAC, converts exceptions to HTTP responses.

### Authentication & RBAC

- Roles: admin, hr, employee
- JWT-based authentication
- Password strength validation
- Force password change on first login

### Payroll Logic

- Precise decimal calculations to avoid floating-point errors
- Supports allowances, deductions, gross/net pay
- Statutory deductions (PAYE, NSSF, NHIF)
- Batch and individual payroll runs
- PDF payslip generation

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/password` - Change password

### Employees
- `GET /employees` - List employees
- `POST /employees` - Create employee
- `GET /employees/{id}` - Get employee details

### Payroll
- `POST /payroll/compute` - Compute payroll
- `POST /payroll/run` - Run and persist payroll
- `POST /payroll/batch` - Batch payroll run

### Audit
- `GET /audit/log` - View audit logs (admin only)

## Testing

Run tests with:
```bash
pytest
```

## Security

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy

## Deployment

For production deployment:
- Set strong `SECRET_KEY`
- Use a production database (PostgreSQL recommended)
- Configure proper CORS settings
- Enable HTTPS
- Set secure environment variables

## Contributing

1. Follow the established architecture and layer responsibilities
2. Add unit and integration tests
3. Update documentation
4. Ensure code passes linting and type checking

## License

[Add license information]
