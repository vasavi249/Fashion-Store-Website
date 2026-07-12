import pymongo
from bson.objectid import ObjectId

# Local MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["fashion_store"]

# Collections
customers_collection = db["customers"]
categories_collection = db["categories"]
products_collection = db["products"]
carts_collection = db["carts"]
orders_collection = db["orders"]

def serialize_doc(doc):
    if not doc:
        return None
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
