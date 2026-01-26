"""
Serializers for ChargeNow API.
"""
from rest_framework import serializers
from .models import User, VanOperator, UserVehicle, ChargingVan, Request, Booking, Payment, Feedback


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_email', 'user_phone', 'user_address', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for User registration"""
    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'user_password', 'user_phone', 'user_address']


class VanOperatorSerializer(serializers.ModelSerializer):
    """Serializer for Van Operator model"""
    class Meta:
        model = VanOperator
        fields = ['operator_id', 'operator_name', 'operator_email', 'operator_phone', 
                  'operator_license_doc', 'operator_status', 'role','is_verified','created_at']
        read_only_fields = ['operator_id', 'created_at']


# class VanOperatorRegistrationSerializer(serializers.ModelSerializer):
#     operator_license_doc = serializers.FileField()
#     def validate_operator_license_doc(self, file):
#         if not file.name.endswith('.pdf' or '.jpg' or '.jpeg'):
#             raise serializers.ValidationError("Only PDF files are allowed")
#         if file.size > 5 * 1024 * 1024:
#             raise serializers.ValidationError("File size must be under 5MB")
#         return file
class VanOperatorRegistrationSerializer(serializers.ModelSerializer):
    operator_license_doc = serializers.FileField()

    def validate_operator_license_doc(self, file):
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']

        if not file.name.lower().endswith(tuple(allowed_extensions)):
            raise serializers.ValidationError(
                "Only PDF or image files (JPG, JPEG, PNG) are allowed"
            )

        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size must be under 5MB")

        return file


    """Serializer for Operator registration"""
    class Meta:
        model = VanOperator
        fields = ['operator_name', 'operator_email', 'operator_password', 
                  'operator_phone', 'operator_license_doc']

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    
    # confirm_password = serializers.CharField()

    # def validate(self, attrs):
    #     if attrs['new_password'] != attrs['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match")
    #     return attrs

class UserVehicleSerializer(serializers.ModelSerializer):
    """Serializer for User Vehicle model"""

    user_name = serializers.CharField(source='user.user_name', read_only=True)


    class Meta:
        model = UserVehicle
        fields = ['vehicle_id', 'user_id','user','user_name', 'vehicle_company', 'vehicle_name', 
                  'vehicle_model', 'vehicle_number', 'created_at']
        read_only_fields = ['vehicle_id', 'created_at']
        extra_kwargs = {
            'vehicle_number': {
                'error_messages': {
                    'unique': 'This vehicle is already registered'
                }
            }
        }


class ChargingVanSerializer(serializers.ModelSerializer):
    """Serializer for Charging Van model"""
    class Meta:
        model = ChargingVan
        fields = ['van_id', 'van_number', 'operator_id', 'battery_capacity', 'created_at']
        read_only_fields = ['van_id', 'created_at']


class RequestSerializer(serializers.ModelSerializer):
    """Serializer for Request model"""
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    operator_name = serializers.CharField(source='operator.operator_name', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)
    class Meta:
        model = Request
        # fields = ['request_id', 'user_id', 'operator_id', 'vehicle_id', 
        #           'user_location', 'request_status', 'request_time']
        fields = [
    'user',
    'operator',
    'vehicle',        
    'user_name',
    'operator_name',
    'vehicle_number',
    'user_latitude',
    'user_longitude',
    'request_status'
]
        read_only_fields = ['request_id', 'request_time']


class BookingSerializer(serializers.ModelSerializer):

    request_id = serializers.IntegerField(write_only=True)
    operator_name = serializers.CharField(
        source='operator.operator_name',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'request_id',
            'operator',
            'operator_name',
            'booking_status',
            'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']
    def create(self, validated_data):
        request_id = validated_data.pop('request_id')

        request_obj = Request.objects.get(request_id=request_id)

        booking = Booking.objects.create(
            request=request_obj,
            **validated_data
        )
        return booking    

# class PaymentSerializer(serializers.ModelSerializer):
#     """Serializer for Payment model"""
#     class Meta:
#         model = Payment
#         fields = ['payment_id', 'booking_id', 'user_id', 'operator_id', 
#                   'amount', 'p_method', 'p_status', 'payment_time']
#         read_only_fields = ['payment_id', 'payment_time']

class PaymentSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source='user.user_name',
        read_only=True
    )

    operator_name = serializers.CharField(
        source='operator.operator_name',
        read_only=True
    )

    booking_id = serializers.IntegerField(
        source='booking.booking_id',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'booking',
            'booking_id',
            'user',
            'user_name',
            'operator',
            'operator_name',
            'amount',
            'p_method',
            'p_status',
            'payment_time'
        ]
        read_only_fields = ['payment_id', 'payment_time']




class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Feedback model"""
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    operator_name = serializers.CharField(source='operator.operator_name', read_only=True)
    class Meta:
        model = Feedback
        fields = ['feedback_id','user_name','operator_name', 'rating', 'comments', 'created_at']
        read_only_fields = ['feedback_id', 'created_at']


class LoginSerializer(serializers.Serializer):
    """Serializer for login request"""
    email = serializers.EmailField()
    password = serializers.CharField()