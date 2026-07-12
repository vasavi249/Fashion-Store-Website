from rest_framework.decorators import api_view
from rest_framework.response import Response
from db import (
    employees_collection, departments_collection, attendance_collection,
    payroll_collection, payslips_collection, serialize_doc
)
from bson.objectid import ObjectId

# ================= EMPLOYEES =================
@api_view(['POST'])
def add_employee(request):
    res = employees_collection.insert_one(request.data)
    return Response({"message": "Employee added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_employees(request):
    employees = list(employees_collection.find())
    return Response([serialize_doc(e) for e in employees])

@api_view(['PUT'])
def update_employee(request, id):
    employees_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Employee updated"})

@api_view(['DELETE'])
def delete_employee(request, id):
    employees_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Employee deleted"})

# ================= DEPARTMENTS =================
@api_view(['POST'])
def add_department(request):
    res = departments_collection.insert_one(request.data)
    return Response({"message": "Department added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_departments(request):
    departments = list(departments_collection.find())
    return Response([serialize_doc(d) for d in departments])

@api_view(['PUT'])
def update_department(request, id):
    departments_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Department updated"})

@api_view(['DELETE'])
def delete_department(request, id):
    departments_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Department deleted"})

# ================= ATTENDANCE =================
@api_view(['POST'])
def add_attendance(request):
    res = attendance_collection.insert_one(request.data)
    return Response({"message": "Attendance marked", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_attendance(request):
    attendance = list(attendance_collection.find())
    return Response([serialize_doc(a) for a in attendance])

@api_view(['PUT'])
def update_attendance(request, id):
    attendance_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Attendance updated"})

@api_view(['DELETE'])
def delete_attendance(request, id):
    attendance_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Attendance deleted"})

# ================= PAYROLL =================
@api_view(['POST'])
def add_payroll(request):
    res = payroll_collection.insert_one(request.data)
    return Response({"message": "Payroll added", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_payroll(request):
    payroll = list(payroll_collection.find())
    return Response([serialize_doc(p) for p in payroll])

@api_view(['PUT'])
def update_payroll(request, id):
    payroll_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Payroll updated"})

@api_view(['DELETE'])
def delete_payroll(request, id):
    payroll_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Payroll deleted"})

# ================= PAYSLIPS =================
@api_view(['POST'])
def add_payslip(request):
    res = payslips_collection.insert_one(request.data)
    return Response({"message": "Payslip generated", "id": str(res.inserted_id)})

@api_view(['GET'])
def get_payslips(request):
    payslips = list(payslips_collection.find())
    return Response([serialize_doc(p) for p in payslips])

@api_view(['PUT'])
def update_payslip(request, id):
    payslips_collection.update_one({"_id": ObjectId(id)}, {"$set": request.data})
    return Response({"message": "Payslip updated"})

@api_view(['DELETE'])
def delete_payslip(request, id):
    payslips_collection.delete_one({"_id": ObjectId(id)})
    return Response({"message": "Payslip deleted"})
