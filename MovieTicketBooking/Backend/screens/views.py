from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import screens_collection
from bson.objectid import ObjectId

def serialize_screen(screen):
    if not screen: return None
    screen['id'] = str(screen['_id'])
    del screen['_id']
    return screen

@api_view(['GET', 'POST'])
def screens_list_create(request):
    if request.method == 'GET':
        theatre_id = request.GET.get('theatreId')
        query = {}
        if theatre_id:
            query['theatreId'] = theatre_id
        screens = list(screens_collection.find(query))
        return Response([serialize_screen(s) for s in screens])
    
    elif request.method == 'POST':
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        data = request.data
        if not all(k in data for k in ['theatreId', 'screenName', 'totalSeats']):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = screens_collection.insert_one(data)
        return Response({"message": "Screen added", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def screen_detail(request, screen_id):
    try:
        obj_id = ObjectId(screen_id)
    except:
        return Response({"error": "Invalid screen ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'GET':
        screen = screens_collection.find_one({"_id": obj_id})
        if not screen:
            return Response({"error": "Screen not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_screen(screen))
        
    elif request.method in ['PUT', 'DELETE']:
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        if request.method == 'PUT':
            screens_collection.update_one({"_id": obj_id}, {"$set": request.data})
            return Response({"message": "Screen updated successfully"})
            
        elif request.method == 'DELETE':
            screens_collection.delete_one({"_id": obj_id})
            return Response({"message": "Screen deleted successfully"})
