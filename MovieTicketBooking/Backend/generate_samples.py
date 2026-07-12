import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import pymongo
from django.contrib.auth.hashers import make_password

MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["movie_ticket_booking"]

print("Clearing old data...")
for col in ['users', 'movies', 'theatres', 'screens', 'shows', 'bookings']:
    db[col].delete_many({})

print("Creating users...")
db.users.insert_many([
    {
        "name": "Admin",
        "email": "admin@movies.com",
        "password": make_password("admin123"),
        "role": "admin"
    },
    {
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "password": make_password("rahul123"),
        "role": "customer"
    },
    {
        "name": "Priya Verma",
        "email": "priya@gmail.com",
        "password": make_password("priya123"),
        "role": "customer"
    }
])
admin_user = db.users.find_one({"email": "admin@movies.com"})
rahul_user = db.users.find_one({"email": "rahul@gmail.com"})
priya_user = db.users.find_one({"email": "priya@gmail.com"})

print("Creating movies...")
db.movies.insert_many([
    {
        "title": "Leo",
        "genre": "Action",
        "language": "Tamil",
        "duration": "2h 44m",
        "rating": "8.2",
        "poster": "https://placehold.co/300x450/1f1f1f/f84464?text=Leo",
        "banner": "https://placehold.co/1200x400/121212/333333?text=Leo"
    },
    {
        "title": "Pushpa 2",
        "genre": "Action",
        "language": "Telugu",
        "duration": "3h 10m",
        "rating": "8.5",
        "poster": "https://placehold.co/300x450/1f1f1f/f84464?text=Pushpa+2",
        "banner": "https://placehold.co/1200x400/121212/333333?text=Pushpa+2"
    },
    {
        "title": "Kalki 2898 AD",
        "genre": "Sci-Fi",
        "language": "Telugu",
        "duration": "3h",
        "rating": "8.9",
        "poster": "https://placehold.co/300x450/1f1f1f/f84464?text=Kalki+2898+AD",
        "banner": "https://placehold.co/1200x400/121212/333333?text=Kalki+2898+AD"
    },
    {
        "title": "Jawan",
        "genre": "Action",
        "language": "Hindi",
        "duration": "2h 50m",
        "rating": "8.3",
        "poster": "https://placehold.co/300x450/1f1f1f/f84464?text=Jawan",
        "banner": "https://placehold.co/1200x400/121212/333333?text=Jawan"
    },
    {
        "title": "Avatar: The Way of Water",
        "genre": "Sci-Fi",
        "language": "English",
        "duration": "3h 12m",
        "rating": "8.7",
        "poster": "https://placehold.co/300x450/1f1f1f/f84464?text=Avatar",
        "banner": "https://placehold.co/1200x400/121212/333333?text=Avatar"
    }
])
movie_leo = db.movies.find_one({"title": "Leo"})
movie_pushpa = db.movies.find_one({"title": "Pushpa 2"})
movie_kalki = db.movies.find_one({"title": "Kalki 2898 AD"})

print("Creating theatres & screens...")
t1_id = db.theatres.insert_one({"theatreName": "PVR Cinemas", "city": "Hyderabad", "address": "Hyderabad"}).inserted_id
s1_id = db.screens.insert_one({"theatreId": str(t1_id), "screenName": "Screen 1", "totalSeats": 120}).inserted_id

t2_id = db.theatres.insert_one({"theatreName": "INOX", "city": "Bengaluru", "address": "Bengaluru"}).inserted_id
s2_id = db.screens.insert_one({"theatreId": str(t2_id), "screenName": "Screen 2", "totalSeats": 100}).inserted_id

t3_id = db.theatres.insert_one({"theatreName": "Cinepolis", "city": "Chennai", "address": "Chennai"}).inserted_id
s3_id = db.screens.insert_one({"theatreId": str(t3_id), "screenName": "Screen 3", "totalSeats": 150}).inserted_id

print("Creating shows...")
show1_id = db.shows.insert_one({
    "movieId": str(movie_leo["_id"]),
    "theatreId": str(t1_id),
    "screenId": str(s1_id),
    "showDate": "2026-07-15",
    "showTime": "10:00",
    "ticketPrice": 250,
    "bookedSeats": ["A1", "A2"]
}).inserted_id

show2_id = db.shows.insert_one({
    "movieId": str(movie_pushpa["_id"]),
    "theatreId": str(t2_id),
    "screenId": str(s2_id),
    "showDate": "2026-07-15",
    "showTime": "14:00",
    "ticketPrice": 300,
    "bookedSeats": ["C5", "C6", "C7"]
}).inserted_id

show3_id = db.shows.insert_one({
    "movieId": str(movie_kalki["_id"]),
    "theatreId": str(t3_id),
    "screenId": str(s3_id),
    "showDate": "2026-07-15",
    "showTime": "19:30",
    "ticketPrice": 350,
    "bookedSeats": []
}).inserted_id

print("Creating bookings...")
db.bookings.insert_many([
    {
        "userId": str(rahul_user["_id"]),
        "showId": str(show1_id),
        "seats": ["A1", "A2"],
        "totalAmount": 500,
        "paymentMethod": "UPI",
        "status": "confirmed"
    },
    {
        "userId": str(priya_user["_id"]),
        "showId": str(show2_id),
        "seats": ["C5", "C6", "C7"],
        "totalAmount": 900,
        "paymentMethod": "UPI",
        "status": "confirmed"
    }
])

print("Data generation complete! You can login with admin@movies.com / admin123")
