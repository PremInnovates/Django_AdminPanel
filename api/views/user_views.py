"""
User views for ChargeNow API.
User profile, vehicles, requests, payments, feedback.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User, UserVehicle, Request, Booking, Payment, Feedback, VanOperator
from ..serializers import (
    UserSerializer, UserVehicleSerializer, RequestSerializer, 
    BookingSerializer, PaymentSerializer, FeedbackSerializer
)
from ..permissions import IsUser


class UserProfileView(APIView):
    """Get and update user profile"""
    permission_classes = [IsUser]
    
    def get(self, request):
        try:
            user = User.objects.get(user_id=request.user['id'])
            serializer = UserSerializer(user)
            return Response({'success': True, 'data': serializer.data})
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            user = User.objects.get(user_id=request.user['id'])
            
            # Update fields
            if 'user_name' in request.data:
                user.user_name = request.data['user_name']
            if 'user_phone' in request.data:
                user.user_phone = request.data['user_phone']
            if 'user_email' in request.data:
                user.user_email = request.data['user_email']    
            if 'user_address' in request.data:
                user.user_address = request.data['user_address']
            
            user.save()
            serializer = UserSerializer(user)
            return Response({'success': True, 'message': 'Profile Updated', 'data': serializer.data})
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== VEHICLE VIEWS ==========

# class UserVehicleListView(APIView):
#     """Get and add user vehicles"""
#     permission_classes = [IsUser]
    
#     def get(self, request):
#         vehicles = UserVehicle.objects.filter(user_id=request.user['id'])
#         serializer = UserVehicleSerializer(vehicles, many=True)
#         return Response({'success': True, 'data': serializer.data})
    
#     def post(self, request):
#         data = request.data.copy()
#         data['user_id'] = request.user['id']
        
        
        
#         serializer = UserVehicleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'success': True, 
#                 'message': 'Vehicle added successfully',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserVehicleListView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        vehicles = UserVehicle.objects.filter(user_id=request.user['id'])
        serializer = UserVehicleSerializer(vehicles, many=True)
        return Response({'success': True, 'data': serializer.data})

    def post(self, request):
        serializer = UserVehicleSerializer(
            data=request.data,
            context={'request': request}   # VERY IMPORTANT
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Vehicle Added Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVehicleDetailView(APIView):
    """Update and delete user vehicle"""
    permission_classes = [IsUser]
    
    def put(self, request, vehicle_id):
        try:
            vehicle = UserVehicle.objects.get(vehicle_id=vehicle_id, user_id=request.user['id'])
            
            if 'vehicle_company' in request.data:
                vehicle.vehicle_company = request.data['vehicle_company']
            if 'vehicle_name' in request.data:
                vehicle.vehicle_name = request.data['vehicle_name']
            if 'vehicle_model' in request.data:
                vehicle.vehicle_model = request.data['vehicle_model']
            if 'vehicle_number' in request.data:
                vehicle.vehicle_number = request.data['vehicle_number']
            
            vehicle.save()
            serializer = UserVehicleSerializer(vehicle)
            return Response({'success': True, 'message': 'Vehicle Updated', 'data': serializer.data})
        except UserVehicle.DoesNotExist:
            return Response({'success': False, 'message': 'Vehicle Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, vehicle_id):
        try:
            vehicle = UserVehicle.objects.get(vehicle_id=vehicle_id, user_id=request.user['id'])
            vehicle.delete()
            return Response({'success': True, 'message': 'Vehicle Deleted Successfully'})
        except UserVehicle.DoesNotExist:
            return Response({'success': False, 'message': 'Vehicle Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== REQUEST VIEWS ==========

class UserRequestListView(APIView):
    """Get user requests and create new request"""
    permission_classes = [IsUser]
    
    def get(self, request):
        requests = Request.objects.filter(user_id=request.user['id'])
        serializer = RequestSerializer(requests, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user['id']
        data['request_status'] = 0  # Pending
        
        serializer = RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True, 
                'message': 'Request Created Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRequestDetailView(APIView):
    """Get request details"""
    permission_classes = [IsUser]
    
    def get(self, request, request_id):
        try:
            req = Request.objects.get(request_id=request_id, user_id=request.user['id'])
            serializer = RequestSerializer(req)
            return Response({'success': True, 'data': serializer.data})
        except Request.DoesNotExist:
            return Response({'success': False, 'message': 'Request Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== BOOKING VIEWS ==========

class UserBookingListView(APIView):
    """Get user bookings"""
    permission_classes = [IsUser]
    
    def get(self, request):
        # Get bookings through requests
        user_requests = Request.objects.filter(user_id=request.user['id']).values_list('request_id', flat=True)
        bookings = Booking.objects.filter(request_id__in=user_requests)
        serializer = BookingSerializer(bookings, many=True)
        return Response({'success': True, 'data': serializer.data})


class UserBookingCancelView(APIView):
    """Cancel a booking"""
    permission_classes = [IsUser]
    
    def put(self, request, booking_id):
        try:
            # Verify booking belongs to user
            user_requests = Request.objects.filter(user_id=request.user['id']).values_list('request_id', flat=True)
            booking = Booking.objects.get(booking_id=booking_id, request_id__in=user_requests)
            
            booking.booking_status = 3  # Cancelled
            booking.save()
            
            return Response({'success': True, 'message': 'Booking Cancelled'})
        except Booking.DoesNotExist:
            return Response({'success': False, 'message': 'Booking Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== PAYMENT VIEWS ==========

class UserPaymentView(APIView):
    """Create payment"""
    permission_classes = [IsUser]
    def get(self, request):
        # Get payments of logged-in user
        payments = Payment.objects.filter(user_id=request.user['id'])
        serializer = PaymentSerializer(payments, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user['id']
        data['p_status'] = 0  # Pending
        
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True, 
                'message': 'Payment Recorded Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# ========== FEEDBACK VIEWS ==========

class UserFeedbackView(APIView):
    """Submit feedback"""
    permission_classes = [IsUser]
    
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user['id']
        
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True, 
                'message': 'Feedback Submitted Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== TRACK OPERATOR ==========

class TrackOperatorView(APIView):
    """Track operator location (simplified)"""
    permission_classes = [IsUser]
    
    def get(self, request, operator_id):
        try:
            operator = VanOperator.objects.get(operator_id=operator_id)
            return Response({
                'success': True, 
                'data': {
                    'operator_id': operator.operator_id,
                    'operator_name': operator.operator_name,
                    'operator_status': operator.operator_status,
                    'is_online': operator.operator_status == 1
                }
            })
        except VanOperator.DoesNotExist:
            return Response({'success': False, 'message': 'Operator Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)
