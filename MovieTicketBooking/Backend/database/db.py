import pymongo
import os
from django.conf import settings

# Default connection string, you can override this with an environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = pymongo.MongoClient(MONGO_URI)
db = client["movie_ticket_booking"]

# Export collections for easy access
users_collection = db["users"]
movies_collection = db["movies"]
theatres_collection = db["theatres"]
screens_collection = db["screens"]
shows_collection = db["shows"]
bookings_collection = db["bookings"]

def get_db():
    return db
