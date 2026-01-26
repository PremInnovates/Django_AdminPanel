"""
Authentication views for ChargeNow API.
"""
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..models import User, VanOperator
from ..serializers import LoginSerializer, UserRegistrationSerializer, VanOperatorRegistrationSerializer, ForgotPasswordSerializer
from ..authentication import generate_token

# from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser

class LoginView(APIView):
    """
    Login endpoint for User & VanOperator.
    Admin login is handled via Django Admin Panel.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # 1️⃣ Try USER login
        try:
            user = User.objects.get(
                user_email=email,
            )
            if not check_password(password, user.user_password):
                raise User.DoesNotExist

            token = generate_token(
                user.user_id,
                user.user_email,
                1,
                user.user_name
            )
            return Response({
                'success': True,
                'message': 'Login Successfully',
                'token': token,
                'user': {
                    'id': user.user_id,
                    'name': user.user_name,
                    'email': user.user_email,
                    'role': 1   # USER
                }
            })
        except User.DoesNotExist:
            pass

        # 2️⃣ Try OPERATOR login
        try:
            operator = VanOperator.objects.get(
                operator_email=email,
            )

            if not check_password(password, operator.operator_password):
                raise VanOperator.DoesNotExist
            token = generate_token(
                operator.operator_id,
                operator.operator_email,
                2,
                operator.operator_name
            )
            return Response({
                'success': True,
                'message': 'Login Successfully',
                'token': token,
                'user': {
                    'id': operator.operator_id,
                    'name': operator.operator_name,
                    'email': operator.operator_email,
                    'role': 2   # OPERATOR
                }
            })
        except VanOperator.DoesNotExist:
            pass

        # 3️⃣ If neither matched
        return Response(
            {'success': False, 'message': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserRegisterView(APIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if User.objects.filter(user_email=serializer.validated_data['user_email']).exists():
            return Response({'success': False, 'message': 'Email already registered'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            user_name=serializer.validated_data['user_name'],
            user_email=serializer.validated_data['user_email'],
            # user_password=serializer.validated_data['user_password'],
            user_password=make_password(serializer.validated_data['user_password']),
            user_phone=serializer.validated_data['user_phone'],
            user_address=serializer.validated_data['user_address'],
            role=1
        )
        
        token = generate_token(user.user_id, user.user_email, 1, user.user_name)
        
        return Response({
            'success': True,
            'message': 'Registration Successfully',
            'token': token,
            'user': {
                'id': user.user_id,
                'name': user.user_name,
                'email': user.user_email,
                'role': 1
            }
        }, status=status.HTTP_201_CREATED)


class OperatorRegisterView(APIView):
    """Van Operator registration endpoint"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    
    def post(self, request):
        # serializer = VanOperatorRegistrationSerializer(data=request.data, files=request.FILES)
        serializer = VanOperatorRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if VanOperator.objects.filter(operator_email=serializer.validated_data['operator_email']).exists():
            return Response({'success': False, 'message': 'Email already registered'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        operator = VanOperator.objects.create(
            operator_name=serializer.validated_data['operator_name'],
            operator_email=serializer.validated_data['operator_email'],
            # operator_password = serializer.validated_data['operator_password'],
            operator_password=make_password(serializer.validated_data['operator_password']),
            operator_phone=serializer.validated_data['operator_phone'],
            operator_license_doc=serializer.validated_data.get('operator_license_doc', ''),
            operator_status=0,
            role=2
        )
        
        token = generate_token(operator.operator_id, operator.operator_email, 2, operator.operator_name)
        
        return Response({
            'success': True,
            'message': 'Registration Successfully',
            'token': token,
            'user': {
                'id': operator.operator_id,
                'name': operator.operator_name,
                'email': operator.operator_email,
                'role': 2
            }
        }, status=status.HTTP_201_CREATED)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        hashed_password = make_password(new_password)

        # 1️⃣ Try USER
        user = User.objects.filter(user_email=email).first()
        if user:
            user.user_password = hashed_password
            user.save()
            return Response({
                'success': True,
                'message': 'Password updated successfully'
            })

        # 2️⃣ Try OPERATOR
        operator = VanOperator.objects.filter(operator_email=email).first()
        if operator:
            operator.operator_password = hashed_password
            operator.save()
            return Response({
                'success': True,
                'message': 'Password updated successfully'
            })

        # 3️⃣ Email not found
        return Response({
            'success': False,
            'message': 'Email not registered'
        }, status=status.HTTP_404_NOT_FOUND)