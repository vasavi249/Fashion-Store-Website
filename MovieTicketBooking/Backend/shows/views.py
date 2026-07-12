from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import shows_collection
from bson.objectid import ObjectId

def serialize_show(show):
    if not show: return None
    show['id'] = str(show['_id'])
    del show['_id']
    return show

@api_view(['GET', 'POST'])
def shows_list_create(request):
    if request.method == 'GET':
        shows = list(shows_collection.find())
        return Response([serialize_show(s) for s in shows])
    
    elif request.method == 'POST':
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        data = request.data
        required = ['movieId', 'theatreId', 'screenId', 'showDate', 'showTime', 'ticketPrice']
        if not all(k in data for k in required):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Optional: initialize bookedSeats as empty array
        data['bookedSeats'] = []
            
        result = shows_collection.insert_one(data)
        return Response({"message": "Show added", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def show_detail(request, show_id):
    try:
        obj_id = ObjectId(show_id)
    except:
        return Response({"error": "Invalid show ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'GET':
        show = shows_collection.find_one({"_id": obj_id})
        if not show:
            return Response({"error": "Show not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_show(show))
        
    elif request.method in ['PUT', 'DELETE']:
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        if request.method == 'PUT':
            shows_collection.update_one({"_id": obj_id}, {"$set": request.data})
            return Response({"message": "Show updated successfully"})
            
        elif request.method == 'DELETE':
            shows_collection.delete_one({"_id": obj_id})
            return Response({"message": "Show deleted successfully"})

@api_view(['GET'])
def shows_by_movie(request, movie_id):
    shows = list(shows_collection.find({"movieId": movie_id}))
    return Response([serialize_show(s) for s in shows])

@api_view(['GET'])
def shows_by_theatre(request, theatre_id):
    shows = list(shows_collection.find({"theatreId": theatre_id}))
    return Response([serialize_show(s) for s in shows])
