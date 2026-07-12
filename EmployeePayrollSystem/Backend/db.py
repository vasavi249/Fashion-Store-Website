import pymongo
from bson.objectid import ObjectId

# Local MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["employee_payroll_system"]

# Collections
employees_collection = db["employees"]
departments_collection = db["departments"]
attendance_collection = db["attendance"]
payroll_collection = db["payroll"]
payslips_collection = db["payslips"]

def serialize_doc(doc):
    if not doc:
        return None
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
