from sqlalchemy.orm import Session
from typing import Optional
from app.models.employee_contacts_details import EmployeeContact

class ContactsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contact(self, email:str)->Optional[EmployeeContact]:
        """Retrieve an EmployeeContact by email."""
        return self.db.query(EmployeeContact).filter(EmployeeContact.email == email).first()
        
    def save(self, contact: EmployeeContact) -> Optional[EmployeeContact]:
        """Save a new or existing EmployeeContact instance to the database."""
        self.db.add(contact)
        return contact