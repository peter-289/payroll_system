from sqlalchemy.orm import Session
from typing import Optional
from app.models.employee_contacts_details import EmployeeContact

class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contact(self, email:str)->Optional[EmployeeContact]:
        return self.db.query(EmployeeContact).filter(EmployeeContact.email == email).first()
        