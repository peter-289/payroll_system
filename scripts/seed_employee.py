import requests


data = {
    "first_name": "Admin",
    "last_name": "Person",
    "username": "hinsei",
    "email": "adminperson@gmail.com",
    "role_name": "admin",
    "date_of_birth": "1990-01-01",
    "department_name": "Engineering",
    "position_title": "Software Engineer",
    "phone_number": "123-456-9890",
    "address": "123 Main St",
    "city": "Metropolis",
    "country": "USA",
    "bank_name": "Bank of Example",
    "account_number": "128456789",
    "account_type": "Checking"
}

URL = "http://localhost:8000/user/create_employee" 

response = requests.post(URL, json=data)
if response.status_code == 200 or response.status_code == 201:
    print("Employee created successfully:", response.json())
else:
    print("Failed to create employee:", response.status_code, response.text)