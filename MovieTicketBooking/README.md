# Movie Ticket Booking Full Stack Application

A complete production-ready full-stack movie ticket booking website built with Django, PyMongo (MongoDB), and Vanilla HTML/CSS/JavaScript.

## Features

- **Customer Portal**: Browse movies, search/filter, view shows, dynamic seat selection, and booking history.
- **Admin Dashboard**: Manage movies, theatres, screens, shows, and bookings. Analytics with Chart.js.
- **Authentication**: Custom JWT-based authentication using PyMongo without relying on Django's ORM.
- **Responsive UI**: Modern BookMyShow inspired dark theme with red accents.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JS (Fetch API)
- **Backend**: Python, Django, Django REST Framework
- **Database**: MongoDB (via PyMongo)

## Setup & Installation

### 1. Prerequisites
- Python 3.8+
- MongoDB instance running locally on `mongodb://localhost:27017/` (or update `MONGO_URI` in `Backend/database/db.py`)

### 2. Backend Setup
1. Navigate to the `Backend` directory:
   ```bash
   cd MovieTicketBooking/Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Django development server:
   ```bash
   python manage.py runserver 8000
   ```

### 3. Generate Sample Data
To populate the database with sample movies, theatres, screens, and an admin user:
1. Ensure the MongoDB instance is running.
2. Ensure you have activated your virtual environment.
3. Run the generator script:
   ```bash
   python generate_samples.py
   ```
   *This creates an admin user (admin@example.com / admin123).*

### 4. Frontend Setup
1. You can serve the `Frontend` folder using any static file server, for example:
   ```bash
   cd MovieTicketBooking/Frontend
   python -m http.server 3000
   ```
2. Or simply open `index.html` in your browser.

## Postman Collection
A `MovieTicketBooking_Postman_Collection.json` is included for testing all the REST API endpoints.

## Directory Structure
```
MovieTicketBooking/
├── Backend/
│   ├── authentication/
│   ├── bookings/
│   ├── config/ (Django settings)
│   ├── dashboard/
│   ├── database/ (PyMongo db.py)
│   ├── movies/
│   ├── screens/
│   ├── shows/
│   ├── theatres/
│   ├── utils/ (JWT decorators)
│   └── generate_samples.py
└── Frontend/
    ├── admin/ (Admin panel pages)
    ├── css/ (Stylesheets)
    ├── js/ (api.js Fetch helper)
    └── (Customer portal HTML files)
```
