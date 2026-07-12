from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import theatres_collection
from bson.objectid import ObjectId

def serialize_theatre(theatre):
    if not theatre: return None
    theatre['id'] = str(theatre['_id'])
    del theatre['_id']
    return theatre

@api_view(['GET', 'POST'])
def theatres_list_create(request):
    if request.method == 'GET':
        theatres = list(theatres_collection.find())
        return Response([serialize_theatre(t) for t in theatres])
    
    elif request.method == 'POST':
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        data = request.data
        if not all(k in data for k in ['theatreName', 'city', 'address']):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = theatres_collection.insert_one(data)
        return Response({"message": "Theatre added", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def theatre_detail(request, theatre_id):
    try:
        obj_id = ObjectId(theatre_id)
    except:
        return Response({"error": "Invalid theatre ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'GET':
        theatre = theatres_collection.find_one({"_id": obj_id})
        if not theatre:
            return Response({"error": "Theatre not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_theatre(theatre))
        
    elif request.method in ['PUT', 'DELETE']:
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        if request.method == 'PUT':
            theatres_collection.update_one({"_id": obj_id}, {"$set": request.data})
            return Response({"message": "Theatre updated successfully"})
            
        elif request.method == 'DELETE':
            theatres_collection.delete_one({"_id": obj_id})
            return Response({"message": "Theatre deleted successfully"})
