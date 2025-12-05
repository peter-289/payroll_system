"""
Database Migration Guide for Payroll Model Improvements
Run these migrations to upgrade from old schema to new schema.
"""

# Migration Steps

## Step 1: Add New Columns
```sql
-- Add version and amendment tracking
ALTER TABLE payrolls ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
ALTER TABLE payrolls ADD COLUMN is_amended BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE payrolls ADD COLUMN amendment_reason TEXT;
ALTER TABLE payrolls ADD COLUMN amended_by INTEGER REFERENCES users(id);

-- Add payment and processing timestamps
ALTER TABLE payrolls ADD COLUMN processed_at TIMESTAMP;
ALTER TABLE payrolls ADD COLUMN paid_at TIMESTAMP;

-- Add payment details
ALTER TABLE payrolls ADD COLUMN payment_method VARCHAR(50);
ALTER TABLE payrolls ADD COLUMN bank_transaction_reference VARCHAR(255);
ALTER TABLE payrolls MODIFY COLUMN bank_transaction_id VARCHAR(100);

-- Add metadata
ALTER TABLE payrolls ADD COLUMN notes TEXT;
ALTER TABLE payrolls ADD COLUMN processing_errors JSON;

-- Add tax breakdown
ALTER TABLE payrolls ADD COLUMN tax_breakdown JSON;
ALTER TABLE payrolls ADD COLUMN tax_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00;

-- Convert existing data types
ALTER TABLE payrolls MODIFY COLUMN basic_salary DECIMAL(12, 2);
ALTER TABLE payrolls MODIFY COLUMN adjusted_base_salary DECIMAL(12, 2);
ALTER TABLE payrolls MODIFY COLUMN department_multiplier DECIMAL(5, 2);
ALTER TABLE payrolls MODIFY COLUMN position_grade_multiplier DECIMAL(5, 2);
ALTER TABLE payrolls MODIFY COLUMN gross_salary DECIMAL(12, 2);
ALTER TABLE payrolls MODIFY COLUMN total_deductions DECIMAL(12, 2);
ALTER TABLE payrolls MODIFY COLUMN net_salary DECIMAL(12, 2);

-- Add total_allowances column
ALTER TABLE payrolls ADD COLUMN total_allowances DECIMAL(12, 2) NOT NULL DEFAULT 0.00;

-- Update status column to use enum
ALTER TABLE payrolls MODIFY COLUMN status VARCHAR(50) NOT NULL;
-- Data conversion: existing values should map to new enum values
UPDATE payrolls SET status = 'paid' WHERE status = 'Paid';
UPDATE payrolls SET status = 'pending' WHERE status = 'Pending';
UPDATE payrolls SET status = 'draft' WHERE status IS NULL OR status = '';
```

## Step 2: Add Constraints
```sql
-- Add check constraints
ALTER TABLE payrolls
ADD CONSTRAINT check_pay_period_valid 
CHECK (pay_period_start <= pay_period_end);

ALTER TABLE payrolls
ADD CONSTRAINT check_basic_salary_positive 
CHECK (basic_salary >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_adjusted_base_positive 
CHECK (adjusted_base_salary >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_gross_positive 
CHECK (gross_salary >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_deductions_positive 
CHECK (total_deductions >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_tax_positive 
CHECK (tax_amount >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_net_positive 
CHECK (net_salary >= 0);

ALTER TABLE payrolls
ADD CONSTRAINT check_net_calculation 
CHECK (gross_salary >= (total_deductions + tax_amount));

-- Add unique constraint for employee + period + version
ALTER TABLE payrolls
ADD CONSTRAINT uq_payroll_employee_period_version 
UNIQUE (employee_id, pay_period_start, pay_period_end, version);
```

## Step 3: Add Indexes
```sql
-- Add performance indexes
CREATE INDEX ix_payroll_employee_period 
ON payrolls(employee_id, pay_period_start, pay_period_end);

CREATE INDEX ix_payroll_status_date 
ON payrolls(status, payment_date);

CREATE INDEX ix_payroll_created_at 
ON payrolls(created_at);
```

## Step 4: Enhance Deduction Model
```sql
-- Deductions table improvements
ALTER TABLE deductions ADD COLUMN deduction_code VARCHAR(20) NOT NULL DEFAULT 'OTHER';
ALTER TABLE deductions ADD COLUMN deduction_type VARCHAR(50) NOT NULL DEFAULT 'voluntary';
ALTER TABLE deductions ADD COLUMN max_amount DECIMAL(12, 2);
ALTER TABLE deductions ADD COLUMN reference_number VARCHAR(100);
ALTER TABLE deductions ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'active';
ALTER TABLE deductions ADD COLUMN is_taxable BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE deductions ADD COLUMN is_recurring BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE deductions ADD COLUMN recurring_end_date DATE;

-- Convert amount from float
ALTER TABLE deductions MODIFY COLUMN amount DECIMAL(12, 2);

-- Add indexes
CREATE INDEX ix_deduction_payroll_id ON deductions(payroll_id);
CREATE INDEX ix_deduction_type_code ON deductions(deduction_code);
CREATE INDEX ix_deduction_status ON deductions(status);
```

## Step 5: Enhance Allowance Model
```sql
-- AllowanceType table improvements
ALTER TABLE allowance_types ADD COLUMN description TEXT;
ALTER TABLE allowance_types ADD COLUMN is_recurring BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE allowance_types ADD COLUMN is_percentage_based BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE allowance_types ADD COLUMN percentage_of VARCHAR(50);
ALTER TABLE allowance_types ADD COLUMN max_amount DECIMAL(12, 2);
ALTER TABLE allowance_types ADD COLUMN min_amount DECIMAL(12, 2);
ALTER TABLE allowance_types ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;

-- Convert amount columns
ALTER TABLE allowance_types MODIFY COLUMN default_amount DECIMAL(12, 2);

-- Allowance table improvements
ALTER TABLE allowances ADD COLUMN code VARCHAR(20);
ALTER TABLE allowances ADD COLUMN is_taxable BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE allowances ADD COLUMN calculation_basis VARCHAR(255);
ALTER TABLE allowances ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'active';
ALTER TABLE allowances ADD COLUMN reference_number VARCHAR(100);

-- Convert amount columns
ALTER TABLE allowances MODIFY COLUMN amount DECIMAL(12, 2);

-- Add indexes
CREATE INDEX ix_allowance_payroll_id ON allowances(payroll_id);
CREATE INDEX ix_allowance_type_id ON allowances(allowance_type_id);
CREATE INDEX ix_allowance_status ON allowances(status);
```

## Step 6: Enhance Tax Model
```sql
-- Tax table improvements
ALTER TABLE tax ADD COLUMN tax_code VARCHAR(20) NOT NULL DEFAULT 'TAX';
ALTER TABLE tax MODIFY COLUMN name VARCHAR(100) NOT NULL;
ALTER TABLE tax MODIFY COLUMN description TEXT;
ALTER TABLE tax ADD COLUMN annual_exemption DECIMAL(12, 2) DEFAULT 0.00;
ALTER TABLE tax ADD COLUMN max_annual_tax DECIMAL(12, 2);
ALTER TABLE tax ADD COLUMN is_cumulative BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE tax MODIFY COLUMN effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE tax ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'active';
ALTER TABLE tax ADD COLUMN is_mandatory BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE tax ADD COLUMN is_deductible BOOLEAN NOT NULL DEFAULT FALSE;

-- Add indexes
CREATE INDEX ix_tax_code ON tax(tax_code);
CREATE INDEX ix_tax_status ON tax(status);
CREATE INDEX ix_tax_effective_date ON tax(effective_date);
```

## Step 7: Enhance Tax Bracket Model
```sql
-- Tax bracket improvements
ALTER TABLE tax_brackets ADD COLUMN description TEXT;
ALTER TABLE tax_brackets ADD COLUMN deductible_amount DECIMAL(12, 2) DEFAULT 0.00;
ALTER TABLE tax_brackets ADD COLUMN effective_from TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE tax_brackets ADD COLUMN effective_to TIMESTAMP;

-- Convert amount columns
ALTER TABLE tax_brackets MODIFY COLUMN min_amount DECIMAL(12, 2);
ALTER TABLE tax_brackets MODIFY COLUMN max_amount DECIMAL(12, 2);
ALTER TABLE tax_brackets MODIFY COLUMN rate DECIMAL(5, 2);

-- Add constraint
ALTER TABLE tax_brackets
ADD CONSTRAINT check_bracket_range 
CHECK (max_amount IS NULL OR max_amount > min_amount);

-- Add indexes
CREATE INDEX ix_tax_bracket_tax_id ON tax_brackets(tax_id);
CREATE INDEX ix_tax_bracket_min_max ON tax_brackets(min_amount, max_amount);
```

## Step 8: Verification Queries
```sql
-- Check data integrity after migration
-- 1. Verify no negative amounts
SELECT COUNT(*) as invalid_salaries FROM payrolls 
WHERE basic_salary < 0 OR gross_salary < 0 OR net_salary < 0;

-- 2. Verify calculation consistency
SELECT COUNT(*) as invalid_calculations FROM payrolls 
WHERE gross_salary < (total_deductions + tax_amount);

-- 3. Check for duplicate payrolls (should be 0 after unique constraint)
SELECT employee_id, pay_period_start, pay_period_end, COUNT(*) 
FROM payrolls 
GROUP BY employee_id, pay_period_start, pay_period_end 
HAVING COUNT(*) > 1;

-- 4. Verify date ranges
SELECT COUNT(*) as invalid_dates FROM payrolls 
WHERE pay_period_start > pay_period_end;

-- 5. Sample data check
SELECT * FROM payrolls LIMIT 5;
```

## Rollback Plan (If Needed)

```sql
-- Drop new constraints
ALTER TABLE payrolls DROP CONSTRAINT IF EXISTS check_pay_period_valid;
ALTER TABLE payrolls DROP CONSTRAINT IF EXISTS uq_payroll_employee_period_version;
-- ... etc

-- Drop new indexes
DROP INDEX IF EXISTS ix_payroll_employee_period;
DROP INDEX IF EXISTS ix_payroll_status_date;
-- ... etc

-- Drop new columns (if using old schema)
ALTER TABLE payrolls DROP COLUMN IF EXISTS version;
ALTER TABLE payrolls DROP COLUMN IF EXISTS is_amended;
-- ... etc
```

## Python Data Migration Script

```python
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Run this after SQL migrations
engine = create_engine('your_database_url')
Session = sessionmaker(bind=engine)
session = Session()

# Example: Migrate float to Decimal
from backend.models.payroll_model import Payroll

for payroll in session.query(Payroll).all():
    # SQLAlchemy automatically handles Decimal conversion
    payroll.basic_salary = Decimal(str(payroll.basic_salary))
    payroll.gross_salary = Decimal(str(payroll.gross_salary))
    payroll.net_salary = Decimal(str(payroll.net_salary))
    session.add(payroll)

session.commit()
print("✅ Migration completed successfully")
```

## Validation Checklist

- [ ] All SQL migrations executed successfully
- [ ] Data integrity checks pass (no negative amounts, invalid calculations)
- [ ] Unique constraints working (no duplicate payrolls)
- [ ] Indexes created and visible in database
- [ ] Application starts without errors
- [ ] Existing payroll queries still work
- [ ] New fields populated with defaults
- [ ] Tests pass
- [ ] Performance metrics baseline established
- [ ] Backup verified

## Timeline

- Development: Update models and services
- Testing: Run full test suite in dev environment
- Staging: Execute migrations on staging database
- Pre-production: Final verification
- Production: Execute during maintenance window
  - Backup database
  - Run migrations
  - Validate data
  - Monitor for errors
  - Fallback ready if needed

---

**Notes:**
- Total downtime: ~5-10 minutes for payroll system
- Backup first!
- Test migrations in dev/staging first
- Have rollback plan ready
