import jwt
import datetime
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def generate_jwt(user_id, role):
    payload = {
        'id': str(user_id),
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except Exception:
        raise AuthenticationFailed('Authentication error')

def get_user_from_request(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('Unauthenticated')
    
    token = auth_header.split(' ')[1]
    payload = decode_jwt(token)
    return payload
