from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from utils.auth import get_user_from_request

def require_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            auth_data = get_user_from_request(request)
            request.user_data = auth_data
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def require_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            auth_data = get_user_from_request(request)
            if auth_data.get('role') != 'admin':
                return Response({"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
            request.user_data = auth_data
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
