from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import movies_collection
from utils.decorators import require_admin
from bson.objectid import ObjectId
import re

def serialize_movie(movie):
    if not movie: return None
    movie['id'] = str(movie['_id'])
    del movie['_id']
    return movie

@api_view(['GET', 'POST'])
def movies_list_create(request):
    if request.method == 'GET':
        movies = list(movies_collection.find())
        return Response([serialize_movie(m) for m in movies])
    
    elif request.method == 'POST':
        # Need to protect with admin, doing it manually since decorator restricts GET too if applied to whole view
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        data = request.data
        required_fields = ['title', 'genre', 'language', 'duration', 'releaseDate', 'poster', 'banner']
        if not all(k in data for k in required_fields):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
            
        result = movies_collection.insert_one(data)
        return Response({"message": "Movie added", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_id):
    try:
        obj_id = ObjectId(movie_id)
    except:
        return Response({"error": "Invalid movie ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'GET':
        movie = movies_collection.find_one({"_id": obj_id})
        if not movie:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_movie(movie))
        
    elif request.method in ['PUT', 'DELETE']:
        from utils.auth import get_user_from_request
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        if request.method == 'PUT':
            movies_collection.update_one({"_id": obj_id}, {"$set": request.data})
            return Response({"message": "Movie updated successfully"})
            
        elif request.method == 'DELETE':
            movies_collection.delete_one({"_id": obj_id})
            # Optionally cascade delete shows, etc.
            return Response({"message": "Movie deleted successfully"})

@api_view(['GET'])
def movie_search(request):
    q = request.GET.get('q', '')
    movies = list(movies_collection.find({"title": {"$regex": q, "$options": "i"}}))
    return Response([serialize_movie(m) for m in movies])

@api_view(['GET'])
def movie_by_genre(request, genre):
    movies = list(movies_collection.find({"genre": {"$regex": genre, "$options": "i"}}))
    return Response([serialize_movie(m) for m in movies])

@api_view(['GET'])
def movie_by_language(request, language):
    movies = list(movies_collection.find({"language": {"$regex": language, "$options": "i"}}))
    return Response([serialize_movie(m) for m in movies])
