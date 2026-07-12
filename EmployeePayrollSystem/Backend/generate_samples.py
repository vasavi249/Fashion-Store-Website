import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from db import (
    employees_collection, departments_collection, attendance_collection,
    payroll_collection, payslips_collection
)
from django.contrib.auth.hashers import make_password

print("Clearing collections...")
for col in [employees_collection, departments_collection, attendance_collection, payroll_collection, payslips_collection]:
    col.delete_many({})

print("Inserting samples...")

employees_collection.insert_many([
    {
        "employee_id": 101,
        "full_name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "phone": "9876543210",
        "department": "Software Development",
        "designation": "Python Developer",
        "joining_date": "2026-01-15",
        "salary": 60000,
        "password": make_password("rahul123"),
        "role": "employee"
    },
    {
        "employee_id": 100,
        "full_name": "Admin Manager",
        "email": "admin@company.com",
        "phone": "9999999999",
        "department": "HR",
        "designation": "HR Admin",
        "joining_date": "2025-01-01",
        "salary": 80000,
        "password": make_password("admin123"),
        "role": "admin"
    }
])

departments_collection.insert_one({
    "department_id": 201,
    "department_name": "Software Development",
    "manager_name": "Anjali Verma",
    "total_employees": 15,
    "location": "Bangalore"
})

attendance_collection.insert_one({
    "attendance_id": 301,
    "employee_name": "Rahul Sharma",
    "attendance_date": "2026-07-15",
    "check_in": "09:00",
    "check_out": "18:00",
    "status": "Present"
})

payroll_collection.insert_one({
    "payroll_id": 401,
    "employee_name": "Rahul Sharma",
    "basic_salary": 60000,
    "bonus": 5000,
    "deductions": 2000,
    "net_salary": 63000,
    "payment_month": "July 2026"
})

payslips_collection.insert_one({
    "payslip_id": 501,
    "employee_name": "Rahul Sharma",
    "payment_date": "2026-07-31",
    "payment_method": "Bank Transfer",
    "payment_status": "Paid",
    "remarks": "Salary credited successfully"
})

print("Sample data generated!")
