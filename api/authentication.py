"""
JWT Authentication for ChargeNow API.
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):
    """Custom JWT Authentication"""
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from "Bearer <token>"
            parts = auth_header.split()
            if parts[0].lower() != 'bearer' or len(parts) != 2:
                return None
            
            token = parts[1]
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Return user info and token payload
            user_data = {
                'id': payload.get('id'),
                'email': payload.get('email'),
                'role': payload.get('role'),
                'name': payload.get('name')
            }
            
            return (user_data, token)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
    
    def authenticate_header(self, request):
        return 'Bearer'


def generate_token(user_id, email, role, name):
    """Generate JWT token for authenticated user"""
    payload = {
        'id': user_id,
        'email': email,
        'role': role,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token
