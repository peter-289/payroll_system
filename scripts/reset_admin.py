import os
import sys
# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.database_setups.database_setup import init_db, SessionLocal
from backend.models.roles_model import Role
from backend.models.user_model import User
from backend.dependancies.security import hash_password, verify_password

if __name__ == '__main__':
    print('\nChecking security.py module:')
    try:
        from passlib.hash import bcrypt
        print('passlib.hash.bcrypt available')
    except ImportError:
        print('passlib.hash.bcrypt NOT available')

    init_db()  # Ensure models are loaded properly
    db = SessionLocal()
    try:
        # Import Role first for proper relationship resolution
        Role  # ensure Role class is registered
        user = db.query(User).filter(User.username=='admin').first()
        if user:
            print('\nHashing flow test:')
            test_pass = 'TestPass123!'
            test_hash = hash_password(test_pass)
            print('Test hash:', test_hash)
            print('Test verify with correct pass:', verify_password(test_pass, test_hash))
            print('Test verify with wrong pass:', verify_password('WrongPass', test_hash))

            print('\nAdmin password update:')
            password = 'AdminPass123!'
            user.password_hash = hash_password(password)
            db.commit()
            print('New admin hash:', user.password_hash)
            print('Password verify with correct pass:', verify_password(password, user.password_hash))
            print('Password verify with wrong pass:', verify_password('WrongPass', user.password_hash))
        else:
            print('Admin user not found')
    finally:
        db.close()