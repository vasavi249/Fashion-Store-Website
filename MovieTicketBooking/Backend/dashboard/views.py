from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import movies_collection, theatres_collection, screens_collection, shows_collection, bookings_collection, users_collection
from utils.auth import get_user_from_request

@api_view(['GET'])
def dashboard_stats(request):
    try:
        auth_data = get_user_from_request(request)
        if auth_data.get('role') != 'admin':
            return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    total_movies = movies_collection.count_documents({})
    total_theatres = theatres_collection.count_documents({})
    total_screens = screens_collection.count_documents({})
    total_shows = shows_collection.count_documents({})
    total_users = users_collection.count_documents({})
    total_bookings = bookings_collection.count_documents({})
    
    # Calculate revenue
    pipeline = [{"$group": {"_id": None, "totalRevenue": {"$sum": "$totalAmount"}}}]
    rev_res = list(bookings_collection.aggregate(pipeline))
    revenue = rev_res[0]['totalRevenue'] if rev_res else 0
    
    return Response({
        "totalMovies": total_movies,
        "totalTheatres": total_theatres,
        "totalScreens": total_screens,
        "totalShows": total_shows,
        "totalUsers": total_users,
        "totalBookings": total_bookings,
        "totalRevenue": revenue,
        "todayRevenue": 0, # Placeholder for simplicity
        "monthlyRevenue": revenue
    })

@api_view(['GET'])
def dashboard_revenue(request):
    # Dummy chart data
    return Response({
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "data": [1000, 2000, 1500, 3000, 2500, 4000]
    })

@api_view(['GET'])
def dashboard_bookings(request):
    # Dummy chart data
    return Response({
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [10, 15, 8, 20, 35, 50, 45]
    })

@api_view(['GET'])
def dashboard_top_movies(request):
    # Dummy data
    return Response([
        {"title": "Inception", "bookings": 150},
        {"title": "Interstellar", "bookings": 120},
        {"title": "The Dark Knight", "bookings": 100}
    ])
