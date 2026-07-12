from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import bookings_collection, shows_collection
from utils.auth import get_user_from_request
from bson.objectid import ObjectId

def serialize_doc(doc):
    if not doc: return None
    doc['id'] = str(doc['_id'])
    del doc['_id']
    return doc

@api_view(['GET', 'POST'])
def bookings_list_create(request):
    try:
        auth_data = get_user_from_request(request)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'GET':
        if auth_data.get('role') == 'admin':
            bookings = list(bookings_collection.find())
        else:
            bookings = list(bookings_collection.find({"userId": auth_data['id']}))
        return Response([serialize_doc(b) for b in bookings])
        
    elif request.method == 'POST':
        # Alias for book_seats essentially
        return book_seats._wrapped_view(request) if hasattr(book_seats, '_wrapped_view') else book_seats(request)

@api_view(['GET', 'PUT', 'DELETE'])
def booking_detail(request, booking_id):
    try:
        auth_data = get_user_from_request(request)
        obj_id = ObjectId(booking_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    booking = bookings_collection.find_one({"_id": obj_id})
    if not booking:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
    if auth_data.get('role') != 'admin' and booking['userId'] != auth_data['id']:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
    if request.method == 'GET':
        return Response(serialize_doc(booking))
        
    elif request.method == 'PUT':
        if auth_data.get('role') != 'admin' and request.data.get('status') != 'cancelled':
             return Response({"error": "Only admin can update booking arbitrarily"}, status=status.HTTP_403_FORBIDDEN)
        
        # If cancelled, release seats
        if request.data.get('status') == 'cancelled' and booking['status'] != 'cancelled':
             shows_collection.update_one(
                 {"_id": ObjectId(booking['showId'])},
                 {"$pullAll": {"bookedSeats": booking['seats']}}
             )
        
        bookings_collection.update_one({"_id": obj_id}, {"$set": request.data})
        return Response({"message": "Booking updated successfully"})
        
    elif request.method == 'DELETE':
        if auth_data.get('role') != 'admin':
            return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        bookings_collection.delete_one({"_id": obj_id})
        return Response({"message": "Booking deleted successfully"})

@api_view(['GET'])
def get_seats(request, show_id):
    try:
        obj_id = ObjectId(show_id)
        show = shows_collection.find_one({"_id": obj_id})
        if not show:
            return Response({"error": "Show not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"bookedSeats": show.get('bookedSeats', [])})
    except:
        return Response({"error": "Invalid show ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'POST'])
def book_seats(request):
    try:
        auth_data = get_user_from_request(request)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    data = request.data
    required = ['showId', 'seats', 'totalAmount', 'paymentMethod']
    if not all(k in data for k in required):
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
        
    # Check if seats are available
    try:
        show_obj_id = ObjectId(data['showId'])
    except:
        return Response({"error": "Invalid show ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    show = shows_collection.find_one({"_id": show_obj_id})
    if not show:
        return Response({"error": "Show not found"}, status=status.HTTP_404_NOT_FOUND)
        
    booked = set(show.get('bookedSeats', []))
    requested = set(data['seats'])
    if booked.intersection(requested):
        return Response({"error": "One or more seats are already booked"}, status=status.HTTP_400_BAD_REQUEST)
        
    # Update show booked seats
    shows_collection.update_one(
        {"_id": show_obj_id},
        {"$addToSet": {"bookedSeats": {"$each": data['seats']}}}
    )
    
    # Create booking
    booking_doc = {
        "userId": auth_data['id'],
        "showId": data['showId'],
        "seats": data['seats'],
        "totalAmount": data['totalAmount'],
        "paymentMethod": data['paymentMethod'],
        "status": "confirmed"
    }
    
    result = bookings_collection.insert_one(booking_doc)
    return Response({
        "message": "Booking successful",
        "bookingId": str(result.inserted_id)
    }, status=status.HTTP_201_CREATED)
