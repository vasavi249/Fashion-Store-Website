from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.db import users_collection
from utils.auth import generate_jwt, get_user_from_request
from django.contrib.auth.hashers import make_password, check_password
from bson.objectid import ObjectId

@api_view(['POST'])
def register(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'customer')

    if not all([name, email, phone, password]):
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if users_collection.find_one({"email": email}):
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)
    
    user = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": hashed_password,
        "role": role
    }
    
    result = users_collection.insert_one(user)
    
    return Response({"message": "User created successfully", "userId": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = users_collection.find_one({"email": email})
    
    if not user or not check_password(password, user['password']):
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    token = generate_jwt(user['_id'], user['role'])
    
    return Response({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "role": user['role']
        }
    })

@api_view(['POST'])
def logout(request):
    return Response({"message": "Logout successful"})

@api_view(['GET', 'PUT'])
def profile(request):
    try:
        auth_data = get_user_from_request(request)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = auth_data['id']
    
    if request.method == 'GET':
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "phone": user.get('phone', ''),
            "role": user['role']
        })
        
    elif request.method == 'PUT':
        data = request.data
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'phone' in data:
            update_data['phone'] = data['phone']
        if 'password' in data and data['password']:
            update_data['password'] = make_password(data['password'])
            
        if update_data:
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            
        return Response({"message": "Profile updated successfully"})
